from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
from user_profile.models import Profile
from django.contrib.auth.forms import AuthenticationForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect("home")
