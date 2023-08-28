from django.contrib.auth import views as auth_view
from django.urls import include, path, reverse_lazy

from . import views

app_name = "users"

urlpatterns = [
    path(
        "password_reset/",
        auth_view.PasswordResetView.as_view(
            success_url=reverse_lazy("users:password_reset_done")
        ),
        name="password_reset",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_view.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("users:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_change/",
        auth_view.PasswordChangeView.as_view(
            success_url=reverse_lazy("users:password_change_done")
        ),
        name="password_change",
    ),
    path("login/", views.LoginView.as_view(), name="login"),
    path("edit_profile/", views.UserUpdateView.as_view(), name="edit_profile"),
    path("", include("django.contrib.auth.urls")),
    path("registration/", views.UserCreateView.as_view(), name="registration"),
]
