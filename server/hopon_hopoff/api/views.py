from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

def test_view(request):
    print(request)
    return Response('dasdsadsadsa')
