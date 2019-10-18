from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash

from user.models import TemporaryPassword
from hub.models import Hub

from user.forms import HubSignUpContactForm, GeneralUserContactForm, TechnicalContactForm

from public.views import contact_view

def password_check(user):
    ''' Check if the user has a TemporaryPassword reference, indicating that that
    the user needs to change their password. '''

    if TemporaryPassword.objects.filter(user=user):
        return False
    return True
@login_required(login_url='/login/', redirect_field_name=None)
@user_passes_test(password_check, login_url='/user/settings_password/', redirect_field_name=None)
def contact(request):

    title = 'Contact'
    choices = [GeneralUserContactForm, TechnicalContactForm, HubSignUpContactForm]
    layout = 'user'
    page_description = []

    return contact_view(request, title, choices, layout, page_description)