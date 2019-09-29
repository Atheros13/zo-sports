"""
Definition of views.
"""

from datetime import datetime
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.http import HttpRequest
from public.forms import ContactForm, EmailForm, PasswordChange
from user.models import CustomUser, UserSignup, PasswordReset

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


def password_reset_request(request):
    assert isinstance(request, HttpRequest)
    message = 'Enter your email address, and we will send you link to reset your password.'

    if request.method == 'POST':

        form = EmailForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            email = f['email']
            c = CustomUser.objects.filter(email=email)
            if c:
                user = c[0]
                p = PasswordReset(user=user)
                unique = False
                while not unique:
                    reference = CustomUser.objects.make_random_password()
                    if not PasswordReset.objects.filter(reference=reference):
                        p.reference = reference
                        p.save()
                        unique = True
                p.send_reset_link()
                return redirect('password_reset_sent')

            else:
                message = '''There is no user account with that email address, 
                please check the address, or use the Contact page to create a new account.'''

    return render(
        request,
        'public/password_reset_request.html',
        {
            'title':'Password Reset',
            'year':datetime.now().year,
            'form':EmailForm(), 'message':message,
        }
    )

def password_reset_sent(request):

    assert isinstance(request, HttpRequest)

    message = 'A link to reset your password has been sent to your email'

    return render(
        request,
        'public/message.html',
        {
            'layout':'public/layout.html',
            'title':'Success',
            'message':message,
            'year':datetime.now().year,
        }
    )

def password_reset(request, reset_reference):
    assert isinstance(request, HttpRequest)

    if request.method == 'GET':

        p = PasswordReset.objects.filter(reference=reset_reference)
        if p:
            user = p[0].user
            email = user.email
            message = 'Please enter your new password below.'
            form = PasswordChange()

        else:
            return render(
                request,
                'public/message.html',
                {
                    'layout':'public/layout.html',
                    'title':'Incorrect Reset Link',
                    'message':'This link has either expired or is incorrect',
                    'year':datetime.now().year,
                }
            )

    elif request.method == 'POST':
        
        user = PasswordReset.objects.filter(reference=reset_reference)[0].user

        form = PasswordChange(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            p1 = f['password1']
            p2 = f['password2']
            if p1 == p2:

                user.set_password(p1)
                user.save()
                reset_list = PasswordReset.objects.filter(user=user)
                for p in reset_list:
                    p.delete()

                return render(
                    request,
                    'public/message.html',
                    {
                        'layout':'public/layout.html',
                        'title':'Success',
                        'message':'Your password has successfully been reset',
                        'year':datetime.now().year,
                    }
                )

            else:
                email = user.email
                message = 'The passwords provided did not match, please try again.'
                form = PasswordChange()

    return render(
        request,
        'public/password_reset.html',
        {
            'title':'Password Reset', 'email':email,
            'message':message, 'form':form,
            'year':datetime.now().year,
        }
    )