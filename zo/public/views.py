"""
Definition of views.
"""

from datetime import datetime
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.http import HttpRequest
from public.forms import ContactForm, EmailForm
from user.models import CustomUser, Signup

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

            unique_check = CustomUser.objects.filter(email=f['email'])

            if contact_type == 'Signup' and not unique_check:
                signup = Signup(firstname=f['firstname'], surname=f['surname'],
                                email=f['email'], phone=f['phone'], message=f['message'])
                signup.save()

                email_message += 'https://112.109.84.57:8000/user/confirm_user_signup/%s' % signup.id

            else:

                error_message = ''
                if f['message'] == '' and contact_type != 'Signup':
                    error_message += 'Please enter a message to be sent. '
                if unique_check and contact_type == 'Signup':
                    error_message += 'A user with the email %s already exists. ' % f['email']
                    f['email'] = ''

                if error_message != '':
                        return render(
                            request,
                            'public/contact.html',
                            {
                                'title':'Contact',
                                'year':datetime.now().year,
                                'form':ContactForm(initial=f),
                                'missing_field':error_message,
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

def password_reset(request):
    assert isinstance(request, HttpRequest)

    message = 'Enter your login email and we will send you link to reset your password'

    return render(
        request,
        'public/password_reset.html', 
        {
            'title':'Reset Password','year':datetime.now().year,
            'form':EmailForm(), 'message':message,
        }
        )