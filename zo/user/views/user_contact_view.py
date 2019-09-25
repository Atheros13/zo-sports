from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash

from user.models import TemporaryPassword
from hub.models import Hub

from user.forms import HubSignUpForm, UserContactForm

class ContactFormChoices():

    ''' An object that contains the button_text, description and form for a Form choice 
    on a Contact page. '''

    def __init__(self, button_text, description, form):

        self.button_text = button_text
        self.description = description
        self.form = form

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

    choices = [ContactFormChoices('General', 
                                  'Click to send a general message', 
                                  HubSignUpForm()),
               ContactFormChoices('Technical', 
                                  'Click for technical issues, please include as much information as possible',
                                  HubSignUpForm()),
               ContactFormChoices('Create Hub', 
                                  "Click to request to create a new Hub, i.e. a School, Club etc. Please make sure the Hub doesn't already exist.",
                                  HubSignUpForm()),]

    return render(
        request,
        'user/user_contact.html',
        {
            'layout': 'public/layout.html',
            'title':'Contact',
            'choices': choices, 'form':choices[0].form,
            'year':datetime.now().year,
        }
    )
