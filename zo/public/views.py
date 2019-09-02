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

    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data

            org_type = f['org_type']
            org_name = f['org_name']
            request_prototype = f['request_prototype']
            firstname = f['firstname']
            surname = f['surname']
            phone = f['phone']
            message = f['message']
            email = f['email']

            email_message = '%s %s\n\nName: %s %s\nPhone: %s\nRequest: %s\n\nMessage: %s' % (org_type, org_name, firstname, surname, phone, request_prototype, message)
            if f['request_signup'] == True:
                email_message += '\n\n112.109.84.57:8001/user/confirm_user_signup/%s/%s/%s' % (email, firstname, surname)

            try:
                send_mail('General Contact', email_message, email, ['info@zo-sports.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('contact_success')

    return render(
        request,
        'public/contact.html',
        {
            'title':'Contact',
            'year':datetime.now().year,
            'form':form,
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