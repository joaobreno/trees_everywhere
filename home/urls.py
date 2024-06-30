from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('environment/profile/', views.profile, name='profile'),
    path('logout/', views.quick_logout, name='quick_logout'),
]