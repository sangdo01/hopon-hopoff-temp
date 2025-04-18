
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from api._serializers.user_serializers import UserSerializer, ProfileSerializer
from database.models import Profile, RefreshToken
from api.ultils import app_response

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
        username = request.data.get('username')
        password = request.data.get('password')
        # user = authenticate(username=username, password=password)
        user = User.objects.filter(username=username).first()
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
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'is_active': user.is_active,
            },
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
        print('request.user', request.user)
        print('request.auth', request.auth)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return app_response(True, serializer.data, status.HTTP_200_OK, len(serializer.data))

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
