"""
URL configuration for expensetracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from public.views_jwt import EmailOrUsernameLoginView
from public.views_password_reset import (
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("public.urls")),
    path("", include("private.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include("public.api_urls")),
    path("api/login/", EmailOrUsernameLoginView.as_view(), name="login"),
    path("api/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "api/password-reset/",
        PasswordResetRequestView.as_view(),
        name="api-password-reset",
    ),
    path(
        "api/password-reset-confirm/",
        PasswordResetConfirmView.as_view(),
        name="api-password-reset-confirm",
    ),
]
