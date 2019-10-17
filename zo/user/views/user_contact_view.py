from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash

from user.models import TemporaryPassword
from hub.models import Hub

from user.forms import HubSignUpContactForm
from public.forms import GeneralContactForm, TechnicalContactForm

from public.general.classes import ContactFormChoice

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

    choices = [GeneralContactForm, TechnicalContactForm, HubSignUpContactForm]

    form = None
    user = request.user
    error_message = ''

    if request.method == 'POST':

        for c in choices:
            if request.POST.get('Choice %s' % c.title):
                form = c
            elif request.POST.get(c.title):
                contact_form = c(request.POST)
                if contact_form.is_valid():
                    check = contact_form.process_contact(user=user)
                    if check != False:
                        return render(
                            request,
                            'public/message.html',
                            {
                                'layout': 'user/layout.html',
                                'title':'Success',
                                'message': 'Your %s request has been sent.' % contact_form.title,
                                'year': datetime.now().year,
                                }
                            )
                    else:
                        pass
    return render(
        request,
        'public/contact.html',
        {
            'layout': 'user/layout.html',
            'title':'Contact',
            'choices': choices, 'form':form,
            'year':datetime.now().year,
            'error_message':error_message,
        }
    )
