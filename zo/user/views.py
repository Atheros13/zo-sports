from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from user.forms import *
from user.models import *

def password_check(user):
    ''' 
    '''
    if user.temp_password:
        print('Password still temporary one')
        pass

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
        name_form = NameForm(request.POST, instance=user.name())

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
            return redirect('settings')

    else:

        custom_user_form = CustomUserForm(instance=user)
        name_form = NameForm(instance=user.name())

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

    if request.method == 'POST':

        custom_user_form = CustomUserForm(request.POST, instance=user)
        name_form = NameForm(request.POST, instance=user.name())

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

    else:

        custom_user_form = CustomUserForm(instance=user)
        name_form = NameForm(instance=user.name())

    return render(
        request,
        'user/settings.html', 
        {
            'title':'Settings','year':datetime.now().year,
            'custom_user_form':custom_user_form,
            'name_form':name_form,
        }
        )

@login_required(login_url='/login/', redirect_field_name=None)
@user_passes_test(password_check, login_url='/user/settings_password/', redirect_field_name=None)
def settings_email(request):
    assert isinstance(request, HttpRequest)

    user = request.user
    message = '''Please be aware that your email is your log in username, 
                and also how you can reset a forgotten password.'''

    if request.method == 'POST':

        email_form = CustomUserEmailForm(request.POST, instance=user)

        if email_form.is_valid():
            email_form.cleaned_data
            email_form.save()
            return redirect('settings')

    else:

        email_form = CustomUserEmailForm(instance=user)

    return render(
        request,
        'user/settings_email.html', 
        {
            'title':'Change Email','year':datetime.now().year,
            'message':message,
            'form':email_form,
        }
        )


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

            signup = SignupForm(request.POST, instance=Signup.objects.filter(pk=signup_id)[0]).save()
            signup.create_custom_user()

        Signup.objects.filter(pk=signup_id).delete()
        
        # maybe redirect to the next signup available
        signup_list = Signup.objects.all()
        if signup_list:
            signup_id = signup_list[0].pk
        else:
            return redirect('profile')

    signup = Signup.objects.filter(pk=signup_id)[0]
    form = SignupForm(instance=signup)

    return render(
        request,
        'user/confirm_user_signup.html',
        {
            'title':'Signup', 'year':datetime.now().year,
            'form': form,
        }
    )
