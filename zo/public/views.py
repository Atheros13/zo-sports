"""
Definition of views.
"""

from datetime import datetime
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.http import HttpRequest
from public.forms import ContactForm, EmailForm, PasswordChange
from user.models import CustomUser, Signup, PasswordReset

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

def contact_new(request):

    pass


def contact_success(request):

    assert isinstance(request, HttpRequest)

    message = 'Thank you for contacting ZO-SPORTS'

    return render(
        request,
        'public/message.html',
        {
            'layout':'public/layout.html',
            'title':'Message Sent',
            'message':message,
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