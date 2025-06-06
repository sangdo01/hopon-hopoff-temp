from django.urls import path
from ._views import user_views


urlpatterns = [
    # User authentication URLs
    path("register", user_views.RegisterView.as_view(), name="register"),
    path("login", user_views.LoginView.as_view(), name="login"),
    path("refresh-token", user_views.RefreshTokenView.as_view(), name="refresh_token"),
    path("logout", user_views.LogoutView.as_view(), name="logout"),
    path("change-password", user_views.ChangePasswordView.as_view(), name="change_password"),
    path("reset-password", user_views.ResetPasswordView.as_view(), name="reset_password"),
    path("reset-password-confirm", user_views.ResetPasswordConfirmView.as_view(), name="reset_password_confirm"),

    path("profile", user_views.ProfileView.as_view(), name="profile"),
    path("user", user_views.UserListView.as_view(), name="user_list"),
]
