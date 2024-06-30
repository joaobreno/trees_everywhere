from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from home.decorator import *
from home.forms import *


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        redirect_url = reverse('profile', args=[])
        return HttpResponseRedirect(redirect_url)

def about(request):
    return render(request, 'about.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                redirect_url = reverse('profile', args=[])
                return HttpResponseRedirect(redirect_url)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1'] 
            user = User.objects.create_user(username=username, password=password)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required(login_url='login')
@profile_user
def profile(request, context_dict):
    return render(request, 'profile.html', context_dict)

