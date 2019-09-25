from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash

from user.models import TemporaryPassword
from hub.models import Hub

from user.forms import HubSignUpForm, UserContactForm

def password_check(user):
    ''' Check if the user has a TemporaryPassword reference, indicating that that
    the user needs to change their password. '''

    if TemporaryPassword.objects.filter(user=user):
        return False
    return True
@login_required(login_url='/login/', redirect_field_name=None)
@user_passes_test(password_check, login_url='/user/settings_password/', redirect_field_name=None)
def contact(request):
    assert isinstance(request, HttpRequest)


    form = HubSignUpForm()
    buttons = [
            ['General', 'Click to send a general message'],
            ['Technical', 'Click for technical issues, please include as much information as possible'],
            ['Create Hub', "Click to request to create a new Hub, i.e. a School, Club etc. Please make sure the Hub doesn't already exist."],
            ]

    return render(
        request,
        'user/contact.html',
        {
            'title':'Contact',
            'buttons': buttons, 'form':form,
            'year':datetime.now().year,
        }
    )
