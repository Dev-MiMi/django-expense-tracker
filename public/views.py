from django.shortcuts import render

# Create your views here.

def get_started(request):
    return render(request, "public/getstarted.html")
