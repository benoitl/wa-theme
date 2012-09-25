"""views functions for the :module:`windriver` django app"""
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from windriver import forms
from windriver import settings

@require_POST
def search_login(request):
    """logs vivisimo search crawler into a
    django regular user account account"""

    if request.META['REMOTE_ADDR'] not in settings.SEARCH_IP_ADDRESSES:
        return HttpResponseForbidden()

    if request.META['HTTP_USER_AGENT'] != settings.SEARCH_USER_AGENT:
        return HttpResponseForbidden()

    form = forms.SearchEngineAuthenticationForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password, method='ldap')
        login(request, user)
        return HttpResponse('Welcome, Crawler')
    else:
        return HttpResponseForbidden()

        

