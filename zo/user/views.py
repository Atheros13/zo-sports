from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required, user_passes_test

from user.forms import *
from user.models import *

def profile_check(user):
    ''' Checks to see if a user has a Profile(), if not
    directs the user to the /settings page where a Profile()
    can be set up. '''
    if user.profile != None:
        return True

@login_required(login_url='/login/', redirect_field_name=None)
@user_passes_test(profile_check, login_url='/profile/settings/', redirect_field_name=None)
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

            for form in all_forms:
                print(form.cleaned_data)

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
        message = 'No profile has been set up, please enter profile details below.'

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