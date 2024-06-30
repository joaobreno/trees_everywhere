from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id': 'yourUsername','required': 'required'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','id': 'yourPassword','required': 'required'}))

    remember = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input','id': 'rememberMe'}))