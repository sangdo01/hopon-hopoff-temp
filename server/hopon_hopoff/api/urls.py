from django.urls import path, include
from . import views

urlpatterns = [
    path("test_view", views.test_view, name="test_view"),
]
