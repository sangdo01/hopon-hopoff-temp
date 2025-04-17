
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from api._serializers.user_serializers import UserSerializer, ProfileSerializer
from database.models import Profile

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "content": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success":  False, "content": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    View for user login.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # login(request, user)
            profile = Profile.objects.get(user=user) if user else None
            data = ProfileSerializer(profile).data if profile else None
            return Response({"success": True, "content": data}, status=status.HTTP_200_OK)
        return Response({"success": False, "error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    """
    View for user logout.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        return Response({"success": True, "message": "Logout successful"}, status=status.HTTP_200_OK)