from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import get_started, RegisterView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("", get_started, name="get_started"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="public/login.html"),
        name="login",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="public/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="public/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="public/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="public/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="public/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        login_required(
            auth_views.PasswordChangeDoneView.as_view(
                template_name="public/password_change_done.html",
            )
        ),
        name="password_change_done",
    ),
]
