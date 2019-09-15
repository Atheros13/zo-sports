from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from user.forms import *
from user.models import *

def person_check(user):
    ''' Checks to see if a user has a Profile(), if not or if they 
    have a Profile() but their gender or date of birth is not included,
    it directs the user to the /settings page where a Profile()
    can be set up.'''
    if user.person != None:
        if user.person.gender != None or user.person.dob != None:
            return True
@login_required(login_url='/login/', redirect_field_name=None)
@user_passes_test(person_check, login_url='/user/settings/', redirect_field_name=None)
def profile(request):
    assert isinstance(request, HttpRequest)
    p = request.user

    return render(
        request,
        'user/profile.html',
        {
            'title':'Profile',
            'year':datetime.now().year,
            'profile':p,
        }
    )

@login_required(login_url='/login/', redirect_field_name=None)
def settings(request):
    assert isinstance(request, HttpRequest)

    user = request.user
    person = user.person
    if person != None:
        name = user.person.name.name
        gender = user.person.gender
    else:
        name = None
        gender = None

    if request.method == 'POST':

        ## remove
        message = 'remove me'

        custom_user_form = CustomUserForm(request.POST, instance=user)

        person = user.person
        fullname_form = FullNameForm(request.POST, instance=name)
        person_gender_form = PersonGenderForm(request.POST, instance=gender)
        person_form = PersonForm(request.POST, instance=person)

        all_forms = [custom_user_form, fullname_form, 
                     person_gender_form, person_form]
        all_valid = True
        for form in all_forms:
            if form.is_valid() == False:
                print(form)
                all_valid = False
            else:
                form.cleaned_data

        if all_valid:

            if person == None:

                fullname = fullname_form.save()
                person_name = PersonName()
                person_name.name = fullname
                person_name.save()

                person_gender = person_gender_form.save()

                user_person = person_form.save(commit=False)
                user_person.name = person_name
                user_person.gender = person_gender
                user_person.save()

                custom_user = custom_user_form.save(commit=False)
                custom_user.person = user_person
                custom_user.save()

            else:

                for form in [fullname_form, person_gender_form, 
                             person_form, custom_user_form]:
                    form.save()

            return redirect('profile')

    else:

        custom_user_form = CustomUserForm(instance=user)
        fullname_form = FullNameForm(instance=name)
        person_gender_form = PersonGenderForm(instance=gender)
        person_form = PersonForm(instance=person)

        if person != None:
            message = 'Profile details can be updated below.'
        else:
            message = 'Profile details are missing, please enter profile details below.'

    return render(
        request,
        'user/settings.html', 
        {
            'title':'Settings','year':datetime.now().year,
            'message':message, 'custom_user_form':custom_user_form,
            'fullname_form':fullname_form, 'person_gender_form':person_gender_form,
            'person_form':person_form,
        }
        )

def confirm_user_signup_check(user):
    
    ''' Checks if the user is zo-sports staff
    '''
    return user.is_staff
def temporary_password():
    
    pass
@login_required(login_url='/login/', redirect_field_name=None)
@user_passes_test(confirm_user_signup_check, login_url='/', redirect_field_name=None)
def confirm_user_signup(request, signup_id):

    assert isinstance(request, HttpRequest)

    if request.method == 'POST':      

        if request.POST.get('signup-accept'):

            signup = SignupForm(request.POST, instance=Signup.objects.filter(pk=signup_id)[0]).save()

        Signup.objects.filter(pk=signup_id).delete()
        
        # maybe redirect to the next signup available
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
