from . import views
from django.urls import path

urlpatterns = [
        path("", views.get_started, name="get_started"),
        ]
