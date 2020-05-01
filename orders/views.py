from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html")
    context = {
        "user": request.user
    }
    return render(request, "orders/main.html")

def logout(request):
    logout(request)
    return render(request, "orders/login.html")
