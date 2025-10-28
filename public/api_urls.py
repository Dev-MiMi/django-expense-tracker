from django.urls import path
from .views_api import RegisterView
from .views_password_reset import PasswordResetRequestView, PasswordResetConfirmView
from .views_jwt import EmailOrUsernameLoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password_reset"),
    path(
        "password-reset-confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("login/", EmailOrUsernameLoginView.as_view(), name="login"),
]
