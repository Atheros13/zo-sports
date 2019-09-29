from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash

from user.forms import *
from user.models import *
from public.forms import PasswordChange, EmailChange

### PROFILE ###

def password_check(user):
    ''' Check if the user has a TemporaryPassword reference, indicating that that
    the user needs to change their password. '''

    if TemporaryPassword.objects.filter(user=user):
        return False
    return True
@login_required(login_url='/login/', redirect_field_name=None)
@user_passes_test(password_check, login_url='/user/settings_password/', redirect_field_name=None)
def profile(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'user/profile.html',
        {
            'title':'Profile',
            'year':datetime.now().year,
            'profile':request.user,
        }
    )

### SETTINGS ###

@login_required(login_url='/login/', redirect_field_name=None)
@user_passes_test(password_check, login_url='/user/settings_password/', redirect_field_name=None)
def settings(request):
    assert isinstance(request, HttpRequest)

    user = request.user

    if request.method == 'POST':
        if request.POST.get('profile'):
            return redirect('settings_profile')
        elif request.POST.get('password'):
            return redirect('settings_password')
        elif request.POST.get('email'):
            return redirect('settings_email')

    choices = []
    choices.append(('profile', 'Update Profile Details',
        'Click to change or update your profile details'))
    choices.append(('password','Change Password',
        'Click to change your current password'))
    choices.append(('email', 'Change Email',
        'Click to change your email address. This will change the email that you use to log in'))

    return render(
        request,
        'user/settings.html', 
        {
            'title':'Settings','year':datetime.now().year,
            'choices':choices,
        }
        )

@login_required(login_url='/login/', redirect_field_name=None)
@user_passes_test(password_check, login_url='/user/settings_password/', redirect_field_name=None)
def settings_profile(request):
    assert isinstance(request, HttpRequest)

    user = request.user

    if request.method == 'POST':

        custom_user_form = CustomUserForm(request.POST, instance=user)
        name_form = NameForm(request.POST, instance=user.name)

        all_forms = [custom_user_form, name_form]
        all_valid = True
        for form in all_forms:
            if form.is_valid() == False:
                all_valid = False
            else:
                form.cleaned_data

        if all_valid:
            for form in [name_form, custom_user_form]:
                form.save()
                return render(
                    request,
                    'public/message.html',
                    {
                        'layout':'user/layout.html',
                        'title':'Details Updated',
                        'message':'Your profile details have successfully been updated.',
                        'year':datetime.now().year,
                    }
                )

    else:

        custom_user_form = CustomUserForm(instance=user)
        name_form = NameForm(instance=user.name)

    return render(
        request,
        'user/settings_profile.html', 
        {
            'title':'Profile Details','year':datetime.now().year,
            'custom_user_form':custom_user_form,
            'name_form':name_form,
        }
        )

@login_required(login_url='/login/', redirect_field_name=None)
def settings_password(request):
    assert isinstance(request, HttpRequest)

    user = request.user
    if not password_check(user):
        message = 'You need to change your temporary password before you can continue.'
    else:
        message = 'Enter your current password, then the password you would like to change it to.'

    if request.method == 'POST':

        current = PasswordConfirm(request.POST)
        new = PasswordChange(request.POST)

        if current.is_valid():
            c = current.cleaned_data
            if user.check_password(c['current_password']):
                if new.is_valid():
                    n = new.cleaned_data
                    p1 = n['password1']
                    p2 = n['password2']
                    if p1 == p2:
                        user.set_password(p1)
                        user.save()
                        t = TemporaryPassword.objects.filter(user=user)
                        if t:
                            for tp in t:
                                tp.delete()
                        update_session_auth_hash(request, request.user)
                        return render(
                            request,
                            'public/message.html',
                            {
                                'layout': 'user/layout.html',
                                'title':'Password Changed',
                                'message':'Your password has successfully been changed.',
                                'year':datetime.now().year,
                            }
                        )
                    else:
                        message = 'Your new password did not match the confirm password, please try again.'
                else:
                    message = 'The values entered for the new password are not valid, please try again.'
            else:
                message = "You have entered an incorrect current password. If you do not know this, click the 'Forgot Password?' link below"

    return render(
        request,
        'user/settings_password.html', 
        {
            'title':'Change Password','year':datetime.now().year,
            'current_password_form':PasswordConfirm(),
            'change_form':PasswordChange(),
            'message':message,
        }
        )

@login_required(login_url='/login/', redirect_field_name=None)
@user_passes_test(password_check, login_url='/user/settings_password/', redirect_field_name=None)
def settings_email(request):
    assert isinstance(request, HttpRequest)

    user = request.user
    message = 'Enter your current password, '
    message += 'then the new email you would like to change your account to (and sign in with).'

    if request.method == 'POST':

        current = PasswordConfirm(request.POST)
        new = EmailChange(request.POST)

        if current.is_valid():
            c = current.cleaned_data
            if user.check_password(c['current_password']):
                if new.is_valid():
                    n = new.cleaned_data
                    e1 = n['email1']
                    e2 = n['email2']
                    if e1 == e2:
                        user.email = e1
                        user.save()
                        return render(
                            request,
                            'public/message.html',
                            {
                                'layout': 'user/layout.html',
                                'title':'Email Changed',
                                'message':'Your email address has successfully been changed.',
                                'year':datetime.now().year,
                            }
                        )
                    else:
                        message = 'Your new email did not match the confirm email, please try again.'
                else:
                    message = 'The value entered for the new email are not valid, please try again.'
            else:
                message = "You have entered an incorrect current password. If you do not know this, click the 'Forgot Password?' link below"

    return render(
        request,
        'user/settings_password.html', 
        {
            'title':'Change Email','year':datetime.now().year,
            'current_password_form':PasswordConfirm(),
            'change_form':EmailChange(),
            'message':message,
        }
        )

### CONFIRM USER SIGNUP ###

def confirm_user_signup_check(user):
    
    ''' Checks if the user is zo-sports staff
    '''
    return user.is_staff
@login_required(login_url='/login/', redirect_field_name=None)
@user_passes_test(confirm_user_signup_check, login_url='/', redirect_field_name=None)
def confirm_user_signup(request, signup_id):

    assert isinstance(request, HttpRequest)

    if request.method == 'POST':      

        if request.POST.get('signup-accept'):

            signup = SignupForm(request.POST, instance=UserSignup.objects.filter(pk=signup_id)[0]).save()
            signup.create_custom_user()

        UserSignup.objects.filter(pk=signup_id).delete()
        
        # If this not the only Signup() waiting for process, go through the next one
        signup_list = UserSignup.objects.all()
        if signup_list:
            signup = signup_list[0]
            return render(
                request,
                'user/confirm_user_signup.html',
                {
                    'title':'Signup', 'year':datetime.now().year,
                    'form': SignupForm(instance=signup),
                }
            )

        else:
            return render(
                request,
                    'public/message.html',
                    {
                    'layout':'user/layout.html',
                    'title':'Complete',
                    'message':'All current signup requests have been  processed.',
                    'year':datetime.now().year,
                }
            )

    s = UserSignup.objects.filter(pk=signup_id)
    if s:
        signup = s[0]

        form = SignupForm(instance=signup)

        return render(
            request,
            'user/confirm_user_signup.html',
            {
                'title':'Signup', 'year':datetime.now().year,
                'form': form,
            }
        )
    else:
        # If this not the only Signup() waiting for process, go through the next one
        signup_list = UserSignup.objects.all()
        if signup_list:
            signup = signup_list[0]
            return render(
                request,
                'user/confirm_user_signup.html',
                {
                    'title':'Signup', 'year':datetime.now().year,
                    'form': SignupForm(instance=signup),
                }
            )
        else:
            return render(
                request,
                    'public/message.html',
                    {
                        'layout':'user/layout.html',
                    'title':'Signup ID Invalid',
                    'message':'There are no current Signup requests to be processed.',
                    'year':datetime.now().year,
                }
            )

### CONFIRM HUB SIGNUP ###

@login_required(login_url='/login/', redirect_field_name=None)
@user_passes_test(confirm_user_signup_check, login_url='/', redirect_field_name=None)
def confirm_hub_signup(request, signup_id):

    pass