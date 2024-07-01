from django.db import models
from django.contrib.auth.models import User as AuthUser
from decimal import Decimal
from allauth.socialaccount.models import SocialAccount
from datetime import datetime
from django.utils import timezone

class Account(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(AuthUser, related_name='accounts')

    def __str__(self):
        return self.name
    
    def members(self):
        return self.users.all()

    def len_members(self):
        members = self.users.all()
        return len(members)
    
    def trees_list(self):
        return PlantedTree.objects.filter(user__accounts=self).order_by('-planted_at')
    
    def len_trees(self):
        return len(self.trees_list())

class Tree(models.Model):
    name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class PlantedTree(models.Model):
    age = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    register = models.DateTimeField(auto_now_add=True, blank=True)
    planted_at = models.DateTimeField(blank=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='planted_trees')
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.tree.name)
    
    @property
    def planted_at_templ(self):
        return self.planted_at.strftime('%d/%m/%Y')
    
    @property
    def age(self):
        if self.planted_at:
            now = timezone.now()
            if timezone.is_naive(self.planted_at):
                self.planted_at = timezone.make_aware(self.planted_at, timezone.get_current_timezone())
            time_difference = now - self.planted_at

            days = time_difference.days
            years = days // 365

            if years < 1:
                return f'{days} dias'
            else:
                return f'{years} anos'
        return None
        

class Profile(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    google_account = models.OneToOneField(SocialAccount, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    about = models.TextField()
    joined = models.DateTimeField(auto_now_add=True)
    job = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True) 
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    @property
    def name_templ(self):
        return self.name if self.name else self.user.username

    @property
    def have_social_urls(self):
        if self.facebook or self.instagram or self.linkedin:
            return True
        else:
            return False
            
    def get_profile_photo(self):
        if self.profile_photo:
            return self.profile_photo.url
        elif self.google_account:
            return self.google_account.extra_data['picture']
        else:
            return None
        
    def trees_list(self):
        return PlantedTree.objects.filter(user=self.user).order_by('-planted_at')
    
    def len_trees(self):
        return len(self.trees_list())