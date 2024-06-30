from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.http import HttpResponseRedirect, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from home.decorator import *
from home.forms import *
from django.contrib import messages


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
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile = context_dict['profile']

            profile.name = profile_form.cleaned_data['name']
            profile.about = profile_form.cleaned_data['about']
            profile.job = profile_form.cleaned_data['job']
            profile.country = profile_form.cleaned_data['country']
            profile.address = profile_form.cleaned_data['address']
            profile.phone = profile_form.cleaned_data['phone']
            profile.email = profile_form.cleaned_data['email']
            profile.facebook = profile_form.cleaned_data['facebook']
            profile.instagram = profile_form.cleaned_data['instagram']
            profile.linkedin = profile_form.cleaned_data['linkedin']

            profile.profile_photo = profile_form.cleaned_data['profile_photo']

            profile.save()
            messages.success(request, 'Alterações do perfil salvas com sucesso!')
            return redirect('profile')
        else:
            messages.error(request, 'Erro no formulário!')
    else:
        profile_form = ProfileForm(profile=context_dict['profile'])
    context_dict['profile_form'] = profile_form
    return render(request, 'profile.html', context_dict)


def quick_logout(request):
    logout(request)
    return redirect('index')
