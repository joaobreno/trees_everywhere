from django.urls import path, include
from . import views
from .autocompletes import *

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('environment/profile/', views.profile, name='profile'),
    path('environment/profile/register/plantedtree', views.edit_planted_tree, name='register-planted-tree'),
    path('environment/profile/edit/plantedtree/<int:id>', views.edit_planted_tree, name='edit-planted-tree'),
    path('logout/', views.quick_logout, name='quick_logout'),
]