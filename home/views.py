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
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PlantedTreeSerializer


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
        
    trees_registered = PlantedTree.objects.filter(user=request.user).order_by('-planted_at')
    accounts = request.user.accounts.all()

    context_dict['profile_form'] = profile_form
    context_dict['planted_trees'] = trees_registered
    context_dict['number_trees'] = len(trees_registered)
    context_dict['accounts'] = accounts
    context_dict['number_accounts'] = len(accounts)
    return render(request, 'profile.html', context_dict)


@login_required(login_url='login')
@profile_user
def edit_planted_tree(request, context_dict, id=None):
    try:
        tree = get_object_or_404(PlantedTree, pk=id) if id else None
    except Exception as e:
        return render(request, 'error-page.html', {'title': 'Not Found 404',
                                                   'code': '404',
                                                   'message': 'Essa página não existe!'})
    if request.method == 'POST':
        form_tree = RegisterPlantedTreeForm(request.POST)
        if form_tree.is_valid():
            if tree:
                planted_tree = tree
            else:
                planted_tree = PlantedTree()

            planted_tree.description = form_tree.cleaned_data['name']
            planted_tree.tree = form_tree.cleaned_data['especie']

            ### CONVERTER DATA
            data_plantio = form_tree.cleaned_data['data_plantio']
            ano, mes, dia = data_plantio.split('-')
            date_format = datetime.datetime(int(ano), int(mes), int(dia))
            planted_tree.planted_at = date_format

            ### LOCALIZAÇÃO
            planted_tree.latitude = form_tree.cleaned_data['latitude']
            planted_tree.longitude = form_tree.cleaned_data['longitude']

            planted_tree.user = request.user

            planted_tree.save()

            messages.success(request, 'Árvore editada com sucesso!' if tree else 'Árvore cadastrada com sucesso!')
            return redirect('profile')

        else:
            messages.error(request, 'Erro no formulário!')
    else:
        if tree:
            form_tree = RegisterPlantedTreeForm(tree=tree)
            if tree.user != request.user:
                return render(request, 'error-page.html', {'title': 'Forbidden 403',
                                                           'code': '403',
                                                           'message': 'Você não pode acessa essa página!'})
        else:
            form_tree = RegisterPlantedTreeForm()
    context_dict['form_tree'] = form_tree
    context_dict['tree'] = tree
    return render(request, 'register-plantedtree.html', context_dict)


@login_required(login_url='login')
@profile_user
def account_view(request, context_dict, id):
    try:
        account = get_object_or_404(Account, pk=id) if id else None
    except Exception as e:
        return render(request, 'error-page.html', {'title': 'Not Found 404',
                                                   'code': '404',
                                                   'message': 'Essa página não existe!'})
    context_dict['account'] = account
    return render(request, 'account.html', context_dict)


def quick_logout(request):
    logout(request)
    return redirect('index')


class UserPlantedTreesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        planted_trees = PlantedTree.objects.filter(user=user)
        serializer = PlantedTreeSerializer(planted_trees, many=True)
        return Response(serializer.data)