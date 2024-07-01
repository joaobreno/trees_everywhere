from django.contrib import admin
from .models import *
# Register your models here.

class TreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'country')

admin.site.register(Account)
admin.site.register(Tree, TreeAdmin)
admin.site.register(PlantedTree)
admin.site.register(Profile, ProfileAdmin)