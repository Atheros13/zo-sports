from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import update_session_auth_hash

from public.forms import GeneralContactForm, TechnicalContactForm, UserSignUpContactForm

from public.general.classes import ContactFormChoice

def contact(request):
    assert isinstance(request, HttpRequest)

    choices = [GeneralContactForm, TechnicalContactForm, UserSignUpContactForm]

    form = choices[0]
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
                                'layout': 'public/layout.html',
                                'title':'Success',
                                'message': 'Your %s request has been sent.' % contact_form.title,
                                'year': datetime.now().year,
                                }
                            )
                    else:
                        form = c
                        error_message = '''That email has already been used to sign up. 
                                        It may take some time for a sign up request to be checked and verified, or 
                                        if you need to reset your password, use the link on the Login Page.'''
    return render(
        request,
        'public/contact.html',
        {
            'layout': 'public/layout.html',
            'title':'Contact',
            'choices': choices, 'form':form,
            'year':datetime.now().year,
            'error_message': error_message,
        }
    )
