from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import logout
from home.models import Profile
from allauth.socialaccount.models import SocialAccount


def profile_user(func):
    def _decorated(request, *args, **kwargs):
        context_dict = {}

        if request.user.is_active:
            profiles = Profile.objects.filter(user=request.user)
            

            if profiles:
                profile = profiles.first()
            else:
                profile = Profile.objects.create(user=request.user)
                user_social_accounts = SocialAccount.objects.filter(user=request.user)
                if user_social_accounts:
                    google_account = user_social_accounts.first()
                    profile.google_account = google_account
                    profile.name = google_account.extra_data['name']
                    profile.email = google_account.extra_data['email']
                    profile.save()
            
            context_dict['profile'] = profile
            context_dict['profile_photo_link'] = None
            context_dict['profile_photo'] = None
            if profile.profile_photo:
                context_dict['profile_photo_link'] = profile.profile_photo.url
            elif profile.google_account:
                context_dict['profile_photo_link'] = profile.google_account.extra_data['picture']
            
            if settings.DEBUG == True:
                return func(request, context_dict, *args, **kwargs)
            else:
                try:
                    return func(request, context_dict, *args, **kwargs)
                except Http404 as e:
                    
                    return render('404.html')
                except Exception as e:

                    return render('500.html')

        else:
            logout(request)
            return HttpResponseRedirect("/login/")

    return _decorated