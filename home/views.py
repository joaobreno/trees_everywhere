from django.contrib.auth.decorators import login_required
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
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
@profile_user
def profile(request, context_dict):
    return render(request, 'profile.html')

