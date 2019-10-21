from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import update_session_auth_hash

from public.forms import GeneralContactForm
from public.forms import UserSignUpContactForm, HubUserSignUpContactForm

def contact_view(request, title, choices, layout, page_description):

    ''' Creates a Contact html page using correctly designed ContactForm forms. '''

    assert isinstance(request, HttpRequest)

    form = None
    layout_html = '%s/layout.html' % layout
    user = request.user
    error_message = ''

    if request.method == 'POST':

        for c in choices:
            if request.POST.get('Choice %s' % c.title):
                form = c
            elif request.POST.get(c.title):
                contact_form = c(request.POST)
                if contact_form.is_valid():
                    check, error_message = contact_form.process_contact()
                    if check:
                        return render(
                            request,
                            'public/message.html',
                            {
                                'layout': layout_html,
                                'title':'Success',
                                'message': 'Your %s request has been sent.' % contact_form.title,
                                'year': datetime.now().year,
                                }
                            )
                else:
                    error_message = ''

    return render(
        request,
        'public/contact.html',
        {
            'layout': layout_html,
            'title': title, 'choices': choices, 'form':form,
            'year':datetime.now().year,
            'error_message': error_message,
            'page_description': page_description,
        }
    )

def contact(request):  

    title = 'Contact'
    choices = [GeneralContactForm]
    layout = 'public'
    page_description = []

    return contact_view(request, title, choices, layout, page_description)

def signup(request):

    title = 'Sign Up'
    choices = [UserSignUpContactForm, HubUserSignUpContactForm]
    layout = 'public'
    page_description = [    
    '''At the moment, ZO-SPORTS is restricting sign ups to authorised sign ups only.''',
    '''This means that each sign up request will be checked by one of the ZO-SPORTS team, and manually 
    accepted or declined (so there will be up to a 24 hour delay).''',
    '''We plan to restrict these initial sign ups to Teachers, Sports/Club Administrators, and other organisation staff 
    that will be responsible for creating and running the Hubs and Tournaments.''', ''' ''',
    '''If you also need to request the creation of a new Hub, choose the 'Sign Up & Hub' option.'''
    ]

    return contact_view(request, title, choices, layout, page_description)
    
