from django.shortcuts import render
from .forms import CustomUserCreation
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Create your views here.


def get_started(request):
    return render(request, "public/getstarted.html")


class RegisterView(CreateView):
    form_class = CustomUserCreation
    template_name = "public/signup.html"
    success_url = reverse_lazy("login")
