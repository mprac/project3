from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . forms import RegisterForm
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

def join(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(index)
    else:
        form = RegisterForm()
    return render(request, "orders/join.html", {'form': form})

def logout(request):
    logout(request)
    return render(request, "orders/login.html")
