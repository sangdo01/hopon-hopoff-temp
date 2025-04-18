from django.urls import path
from ._views import user_views


urlpatterns = [
    # User authentication URLs
    path("register", user_views.RegisterView.as_view(), name="register"),
    path("login", user_views.LoginView.as_view(), name="login"),
    path("logout", user_views.LogoutView.as_view(), name="logout"),
    path("profile", user_views.ProfileView.as_view(), name="profile"),
    path("user", user_views.UserListView.as_view(), name="user_list"),
]
