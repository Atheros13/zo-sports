from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email','is_staff')

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('email', 'is_staff')


class FullNameForm(forms.ModelForm):

    class Meta:
        model = FullName
        fields = ['firstname', 'middlenames', 'surname', 'preferred_name']

class PersonGenderForm(forms.ModelForm):

    class Meta:
        model = PersonGender
        fields = ['gender']

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['dob']

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['line1', 'line2', 'line3', 'town_city', 
                  'postcode', 'country']

class ContactDetailsForm(forms.ModelForm):

    class Meta:
        model = ContactDetails
        fields = ['phone_landline', 'phone_mobile', 'email']
