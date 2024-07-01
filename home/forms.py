from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import re
from django.template.defaultfilters import filesizeformat
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from home.models import *
from dal import autocomplete

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
    
    
def get_country_choices():
    choices = [('', '(Vazio)')]
    with open('countries.txt') as file: 
        countries = file.readlines()
    for country in countries:
        choices.append((country.strip(), country.strip()))
    return choices

def validate_facebook_url(value):
    if not re.match(r'^https?://(www\.)?facebook.com/', value):
        raise ValidationError('A URL deve ser do Facebook.')

def validate_instagram_url(value):
    if not re.match(r'^https?://(www\.)?instagram.com/', value):
        raise ValidationError('A URL deve ser do Instagram.')

def validate_linkedin_url(value):
    if not re.match(r'^https?://(www\.)?linkedin.com/', value):
        raise ValidationError('A URL deve ser do LinkedIn.')
    
def validate_file_size(value):
    filesize = value.size
    if filesize > 200 * 1024:  # 200KB
        raise ValidationError(_('O arquivo enviado possui %(filesize)s. O tamanho máximo permitido é de 200KB.'),params={'filesize': filesizeformat(filesize)},)

class ProfileForm(forms.Form):
    name = forms.CharField(label='Nome',
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    about = forms.CharField(label='Sobre',
                            required=False,
                            widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px'}))
    
    job = forms.CharField(label='Ocupação',
                          required=False,
                          max_length=100,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    country = forms.ChoiceField(label='País',
                                choices=get_country_choices(),
                                widget=forms.Select(attrs={'class': 'form-control'}))
    
    address = forms.CharField(label='Endereço de Residência',
                              required=False,
                              max_length=100,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    phone = forms.CharField(label='Telefone',
                            required=False,
                            max_length=20,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    email = forms.EmailField(label='E-mail',
                             required=False,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    facebook = forms.URLField(label='Perfil Facebook',
                              required=False,
                              validators=[validate_facebook_url, URLValidator()],
                              widget=forms.URLInput(attrs={'class': 'form-control'}))
    
    instagram = forms.URLField(label='Perfil Instagram',
                               required=False,
                               validators=[validate_instagram_url, URLValidator()],
                               widget=forms.URLInput(attrs={'class': 'form-control'}))
    
    linkedin = forms.URLField(label='Perfil LinkedIn',
                              required=False,
                              validators=[validate_linkedin_url, URLValidator()],
                              widget=forms.URLInput(attrs={'class': 'form-control'}))
    
    profile_photo = forms.ImageField(label='Foto do Perfil',
                                     required=False,
                                     widget=forms.FileInput(attrs={'class': 'd-none', 'type':"file", 'name': "profile_photo", 'id': "id_profile_photo", 'accept': 'image/jpeg, image/png, image/jpg'}))
    
    def clean_profile_photo(self):
        profile_photo = self.cleaned_data.get('profile_photo', False)
        if profile_photo:
            result = validate_file_size(profile_photo)
        return profile_photo

    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile', None)
        super(ProfileForm, self).__init__(*args, **kwargs)

        if profile:
            self.fields['name'].initial = profile.name
            self.fields['about'].initial = profile.about
            self.fields['job'].initial = profile.job
            self.fields['country'].initial = profile.country
            self.fields['address'].initial = profile.address
            self.fields['phone'].initial = profile.phone
            self.fields['email'].initial = profile.email
            self.fields['facebook'].initial = profile.facebook
            self.fields['instagram'].initial = profile.instagram
            self.fields['linkedin'].initial = profile.linkedin
            self.fields['profile_photo'].initial = profile.profile_photo



class RegisterPlantedTreeForm(forms.Form):

    # name = forms.ModelMultipleChoiceField(queryset=Tree.objects.all(),
    #                                       widget=autocomplete.ModelSelect2(url='trees_autocomplete/',
    #                                                                        attrs={'class': 'form-control', 'type': "text", 'placeholder': "Árvore"}))

    name = forms.CharField(label='Nome',
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'type': "text", 'placeholder': "Nome (Apelido)"}))
    
    especie = forms.ModelChoiceField(required=True,
                                     queryset=Tree.objects.all(),
                                     empty_label= '(Selecione a espécie da árvore plantada)',
                                     widget= forms.Select(attrs={'class':'form-select', 'type': "text", 'placeholder': "Árvore"}))
    

    data_plantio = forms.CharField(required=True,
                                   widget=forms.TextInput(attrs={'type':"date", 'class': "form-control", 'placeholder': "Data de Plantio"}))
    
    latitude = forms.DecimalField(label='Latitude',
                                  required=True,
                                  max_digits=25,
                                  decimal_places=22,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Latitude'}))
    

    longitude = forms.DecimalField(label='Longitude',
                                   required=True,
                                   max_digits=25,
                                   decimal_places=22,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Longitude'}))
    
    def clean_latitude(self):
        latitude = self.cleaned_data['latitude']
        try:
            float(latitude)  # Tenta converter para float
        except ValueError:
            raise ValidationError('Por favor, insira um valor numérico para a latitude.')

        return latitude

    def clean_longitude(self):
        longitude = self.cleaned_data['longitude']
        try:
            float(longitude)  # Tenta converter para float
        except ValueError:
            raise ValidationError('Por favor, insira um valor numérico para a longitude.')

        return longitude


    def __init__(self, *args, **kwargs):
        tree = kwargs.pop('tree', None)
        super(RegisterPlantedTreeForm, self).__init__(*args, **kwargs)

        if tree:
            self.fields['name'].initial = tree.description
            self.fields['especie'].initial = tree.tree
            self.fields['data_plantio'].initial = tree.planted_at.strftime("%Y-%m-%d")
            self.fields['latitude'].initial = tree.latitude
            self.fields['longitude'].initial = tree.longitude

