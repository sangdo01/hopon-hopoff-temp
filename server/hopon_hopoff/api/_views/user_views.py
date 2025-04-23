
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from api._serializers.user_serializers import UserSerializer, ProfileSerializer
from database.models import Profile, RefreshToken, PasswordResetToken
from api.ultils import app_response, get_UI_URL, load_table_params
from api.controllers.user_controllers import process_user_data
from django.conf import settings

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return app_response(True, serializer.data, status.HTTP_201_CREATED)
        return app_response(False, serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    """
    View for user login.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        # user = authenticate(username=username, password=password)
        user = User.objects.filter(email=email).first()
        if user and not user.check_password(password):
            return app_response(False, "Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)
        if not user:
            return app_response(False, "Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)
        # Create or retrieve the token for the user
        token, _ = Token.objects.get_or_create(user=user)

        # Create a refresh token
        refresh_token, _ = RefreshToken.objects.get_or_create(user=user)
        if refresh_token.is_expired():
            refresh_token.delete()
            refresh_token = RefreshToken.objects.create(user=user)

        profile = Profile.objects.get(user=user) if user else None
        data = ProfileSerializer(profile).data if profile else None
        response = {
            'access_token': token.key,
            'refresh_token': refresh_token.key,
            'profile': data
        }
        return app_response(True, response, status.HTTP_200_OK)
    
class RefreshTokenView(APIView):
    """
    View for refreshing the access token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token_key = request.data.get('refresh_token')
        if not refresh_token_key:
            return app_response(False, "Refresh token is required", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh_token = RefreshToken.objects.get(key=refresh_token_key)
            if refresh_token.is_expired():
                refresh_token.delete()
                return app_response(False, "Refresh token has expired", status=status.HTTP_401_UNAUTHORIZED)
            
            # Create a new access token
            token, _ = Token.objects.get_or_create(user=refresh_token.user)
            return app_response(True, {'access_token': token.key}, status=status.HTTP_200_OK)
        except RefreshToken.DoesNotExist:
            return app_response(False, "Invalid refresh token", status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    """
    View for user logout.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            if token:
                token.delete()
            request.user.auth_token.delete()

            # Delete the refresh token
            RefreshToken.objects.filter(user=request.user).delete()

        except Token.DoesNotExist:
            return app_response(False, "Token does not exist", status=status.HTTP_400_BAD_REQUEST) 
        return app_response(True, "Logout successful", status=status.HTTP_200_OK)
    
class ChangePasswordView(APIView):
    """
    View for changing user password.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return app_response(False, "Old password is incorrect", status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return app_response(True, "Password changed successfully", status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    """
    View for resetting user password.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            return app_response(False, "User with this email does not exist", status=status.HTTP_400_BAD_REQUEST)
        
        password_reset_token = PasswordResetToken.objects.create(user=user)
        reset_link = f"{get_UI_URL()}/profile/reset-password-confirm?token={password_reset_token.token}"

        try:
            subject = "Password Reset Request"
            from_email = settings.DEFAULT_FROM_EMAIL
            to = [email]
            text_content = f'Click the link to reset your password: {reset_link}'
            html_content = render_to_string(
                'email/forgot-password.html',
                {'reset_link': reset_link, 'full_name': user.get_full_name()}
            )
            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            # send_mail(
            #     subject,
            #     text_content,
            #     from_email,
            #     to,
            #     fail_silently=False,
            # )
        except Exception as e:
            print(f"Error sending email: {e}")
            return app_response(False, f"Failed to send email: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return app_response(True, "Password reset link sent to your email", status=status.HTTP_200_OK)
    
class ResetPasswordConfirmView(APIView):
    """
    View for confirming password reset.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        # Validate the token and reset the password
        password_reset_token = PasswordResetToken.objects.filter(token=token).first()
        if not password_reset_token:
            return app_response(False, "Invalid or expired token", status=status.HTTP_400_BAD_REQUEST)
        
        user = password_reset_token.user
        user.set_password(new_password)
        user.save()

        password_reset_token.delete()  # Delete the token after use

        password_reset_token_user = PasswordResetToken.objects.filter(user=user)
        if password_reset_token_user.exists():
            password_reset_token_user.delete()
        # Optionally
        RefreshToken.objects.filter(user=user).delete()
        # Optionally
        Token.objects.filter(user=user).delete()
        return app_response(True, "Password reset successfully", status=status.HTTP_200_OK)

class ProfileView(APIView):
    """
    View for user profile.
    """
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user = request.user
        if user.is_authenticated:
            profile = Profile.objects.get(user=user) if user else None
            data = ProfileSerializer(profile).data if profile else None
            return app_response(True, data, status=status.HTTP_200_OK)
        return app_response(False, "User not authenticated", status=status.HTTP_401_UNAUTHORIZED)
    
class UserListView(APIView):
    """
    View for user list.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # test commit
        print('request.user', request.user)
        print('request.auth', request.auth)
        (page, page_size, search, sort_by, sort_order, filters) = load_table_params(request)
        (data, total) = process_user_data(page, page_size, search, sort_by, sort_order, filters)
        return app_response(True, data, status.HTTP_200_OK, total)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return app_response(True, serializer.data, status.HTTP_201_CREATED)
        return app_response(False, serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return app_response(True, serializer.data, status.HTTP_200_OK)
        return app_response(False, serializer.errors, status=status.HTTP_400_BAD_REQUEST)
