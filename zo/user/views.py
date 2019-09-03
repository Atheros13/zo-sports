from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required, user_passes_test

from user.forms import *
from user.models import *

def profile_check(user):
    ''' Checks to see if a user has a Profile(), if not or if they 
    have a Profile() but their gender or date of birth is not included,
    it directs the user to the /settings page where a Profile()
    can be set up.'''
    if user.profile != None:
        if user.profile.person.gender != None or user.profile.person.dob != None:
            return True
@login_required(login_url='/login/', redirect_field_name=None)
@user_passes_test(profile_check, login_url='/user/settings/', redirect_field_name=None)
def profile(request):
    assert isinstance(request, HttpRequest)
    p = request.user.profile

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

    if request.method == 'POST':

        fullname_form = FullNameForm(request.POST)
        person_gender_form = PersonGenderForm(request.POST)
        person_form = PersonForm(request.POST)
        address_form = AddressForm(request.POST)
        contact_details_form = ContactDetailsForm(request.POST)

        all_forms = [fullname_form, person_gender_form, person_form,
                   address_form, contact_details_form]
        all_valid = True
        for form in all_forms:
            if form.is_valid() == False:
                all_valid = False

        if all_valid:

            f = form.cleaned_data

            # update 

    if user.profile:
        p = user.profile
        fullname_form = FullNameForm(instance=p.person.name.name)
        person_gender_form = PersonGenderForm(instance=p.person.gender.gender)
        person_form = PersonForm(instance=p.person)
        address_form = AddressForm(instance=p.contact_details.address)
        contact_details_form = ContactDetailsForm(instance=p.contact_details)
        message = 'Profile details can be updated below.'
    else:
        fullname_form = FullNameForm()
        person_gender_form = PersonGenderForm()
        person_form = PersonForm()
        address_form = AddressForm()
        contact_details_form = ContactDetailsForm(initial={'email': user.email})
        message = 'Profile details are missing, please enter profile details below.'

    return render(
        request,
        'user/settings.html', 
        {
            'title':'Settings','year':datetime.now().year,
            'message':message,
            'fullname_form':fullname_form, 'person_gender_form':person_gender_form,
            'person_form':person_form, 'address_form':address_form,
            'contact_details_form':contact_details_form,
        }
        )

def confirm_user_signup_check(user):
    
    ''' Checks if the user is zo-sports staff
    '''
    return user.is_staff
@login_required(login_url='/login/', redirect_field_name=None)
@user_passes_test(confirm_user_signup_check, login_url='/', redirect_field_name=None)
def confirm_user_signup(request, email, firstname, surname):

    assert isinstance(request, HttpRequest)

    return render(
        request,
        'user/confirm_user_signup.html',
        {
            'title':'Signup', 'year':datetime.now().year,
            'message':'Signup', 'email':email, 'firstname':firstname,
            'surname':surname,
        }
    )