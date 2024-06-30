from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re

### FORM DO LOGIN
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id': 'yourUsername','required': 'required'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','id': 'yourPassword','required': 'required'}))

    remember = forms.BooleanField(required=False,
                                  widget=forms.CheckboxInput(attrs={'class': 'form-check-input','id': 'rememberMe'}))
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Usuário ou senha incorretos!')
        
        return cleaned_data
    
    
### FORM DE CADASTRO
class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','required': 'required'}))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','required': 'required'}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','required': 'required'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username já existente! Por favor, escolha outro username.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        
        # Check password length and complexity
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        
        if not re.search(r'\d', password1):
            raise forms.ValidationError("Senha deve conter ao menos um número.")
        
        if not re.search(r'[A-Za-z]', password1):
            raise forms.ValidationError("Senha deve conter ao menos uma letra.")

        return password2

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data