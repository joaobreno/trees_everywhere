from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import logout


def profile_user(func):
    def _decorated(request, *args, **kwargs):
        context_dict = []

        if request.user.is_active:

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