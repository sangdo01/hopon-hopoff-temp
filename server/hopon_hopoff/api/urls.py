from django.urls import path
from ._views import user_views


urlpatterns = [
    # User authentication URLs
    path("register", user_views.RegisterView.as_view(), name="register"),
    path("login", user_views.LoginView.as_view(), name="login"),
    path("logout", user_views.LogoutView.as_view(), name="logout"),
]
