from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import UserEditForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect('users:profile')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('users:profile')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def user_profile(request):
    user = request.user  # Отримання поточного користувача
    context = {
        'user': user
    }
    return render(request, 'user_profile.html', context)


@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('users:login')


