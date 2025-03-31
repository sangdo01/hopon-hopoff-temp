from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

@api_view(['GET'])
def test_view(request):
    return Response({'message': 'Hello, Django REST!'}, status=status.HTTP_200_OK)