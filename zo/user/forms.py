from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from user.models import *

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email','is_staff', 'is_huttscience')

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('email', 'is_staff', 'is_huttscience')


class SignupForm(forms.ModelForm):

    class Meta:
        model = Signup
        fields = ['firstname', 'surname', 'phone', 'email', 'is_staff', 'message']

class CustomUserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'dob', 'gender']

class CustomUserEmailForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['email']


class NameForm(forms.ModelForm):

    class Meta:
        model = Name
        fields = ['firstname', 'middlenames', 'surname', 'preferred_name']


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['line1', 'line2', 'line3', 'town_city', 
                  'postcode', 'country']

class ContactDetailsForm(forms.ModelForm):

    class Meta:
        model = ContactDetails
        fields = ['phone_landline', 'phone_mobile', 'email']
