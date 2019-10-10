from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import update_session_auth_hash

from public.forms import GeneralContactForm, TechnicalContactForm, UserSignUpContactForm

from public.general.classes import ContactFormChoice

def signup(request):
    assert isinstance(request, HttpRequest)

    page_description = ['''At the moment, ZO-SPORTS is restricting sign ups to authorised sign ups only. 
    This means that each sign up request will be checked by one of the ZO-SPORTS team, and manually 
    accepted or declined (so there will be up to a 24 hour delay). 
    We plan to restrict these initial sign ups to Teachers, Sports/Club Administrators, and other organisation staff 
    that will be resonsible for creating and running the Hubs and Tournaments.''',
    '''If you also need to request the creation of a new Hub, choose the 'Sign Up & Hub' option.''']

    choices = [GeneralContactForm, TechnicalContactForm]

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

    return render(
        request,
        'public/contact.html',
        {
            'layout': 'public/layout.html',
            'title':'Authorised Sign Up Request ',
            'choices': choices, 'form':form,
            'year':datetime.now().year,
            'error_message': error_message,
            'page_description': page_description,
        }
    )
