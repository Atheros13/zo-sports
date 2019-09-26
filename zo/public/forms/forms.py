
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.EmailField(widget=forms.EmailInput({
                                   'class': 'form-control',
                                   'placeholder': 'Email'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class EmailForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput({
                                   'class': 'form-control',
                                   'placeholder': 'Email'}))

class EmailChange(forms.Form):

    email1 = forms.EmailField(label=_("New Email"),widget=forms.EmailInput({
                                   'class': 'form-control',
                                   'placeholder': 'Email'}))
    email2 = forms.EmailField(label=_("Confirm New Email"),
                              widget=forms.EmailInput({
                                   'class': 'form-control',
                                   'placeholder': 'Email'}))

class PasswordChange(forms.Form):

    password1 = forms.CharField(label=_("New Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
    password2 = forms.CharField(label=_("Confirm New Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

