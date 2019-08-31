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

            org_type = form.cleaned_data['org_type']
            org_name = form.cleaned_data['org_name']
            request = form.cleaned_data['request']
            fullname = form.cleaned_data['fullname']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']

            email_message = '%s %s\n\nName: %s\nPhone: %s\nRequest: %s\n\nMessage: %s' % (org_type, org_name, fullname, phone, request, message)

            email = form.cleaned_data['email']

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