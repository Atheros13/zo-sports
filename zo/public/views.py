"""
Definition of views.
"""

from datetime import datetime
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.http import HttpRequest
from public.forms import ContactForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'public/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'public/about.html',
        {
            'title':'About',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':

        form = ContactForm(request.POST)

        if form.is_valid():

            f = form.cleaned_data
            contact_type = f['contact_type']
            email_message = 'Name: %s %s\n' % (f['firstname'], f['surname'])
            email_message += 'Email: %s\nPhone: %s\n' % (f['email'], f['phone'])
            email_message += 'Message: %s\n\n' % f['message']
            if contact_type == 'Signup':
                message = f['message'].replace('/', '')
                email_message += 'https://112.109.84.57:8000/user/confirm_user_signup'
                email_message += '/%s/%s/%s/=%s' % (f['email'],f['firstname'],
                                                    f['surname'], message)
            else:
                if f['message'] == '':
                        return render(
                            request,
                            'public/contact.html',
                            {
                                'title':'Contact',
                                'year':datetime.now().year,
                                'form':ContactForm(initial=f),
                                'missing_field':'You have not filled in the Message field',
                            }
                            )

            send_mail(contact_type, email_message,
                      f['email'], ['info@zo-sports.com'])

            return redirect('contact_success')


    return render(
        request,
        'public/contact.html',
        {
            'title':'Contact',
            'year':datetime.now().year,
            'form':ContactForm(initial={'contact_type':'General'}),
            'missing_field':'',
        }
    )

def contact_success(request):

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'public/contact_success.html',
        {
            'title':'Success',
            'year':datetime.now().year,
        }
    )