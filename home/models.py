from django.db import models
from django.contrib.auth.models import User as AuthUser
from decimal import Decimal
from allauth.socialaccount.models import SocialAccount

class Account(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(AuthUser, related_name='accounts')

    def __str__(self):
        return self.name

class Tree(models.Model):
    name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class PlantedTree(models.Model):
    age = models.IntegerField()
    planted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='planted_trees')
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.tree.name)

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
            