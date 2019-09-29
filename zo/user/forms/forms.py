from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from user.models import *
from hub.models import HubSignUp
from django.utils.translation import ugettext_lazy as _

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
        model = UserSignup
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

class PasswordConfirm(forms.Form):
    ''' Added to forms for extra security, allows a signed in user
    to confirm their password before performing a potentially
    security risk action i.e. changing email or password. '''

    current_password = forms.CharField(label=_("Current Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Current Password'}))
