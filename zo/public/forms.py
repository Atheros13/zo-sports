"""
Definition of forms.
"""

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

class ContactForm(forms.Form):

    CHOICES_ORGANISATION_TYPE = [
        ('School', 'School'), ('Club', 'Club'), 
        ('Other Organisation','Other Organisation'),
        ]

    org_type = forms.ChoiceField(label='Organisation Type', choices=CHOICES_ORGANISATION_TYPE)
    org_name = forms.CharField(label="Organisation Name", max_length=50, required=True)
    request = forms.BooleanField(label="Request Prototype", required=False)
    fullname = forms.CharField(label="Name", max_length=50, required=True)
    email = forms.EmailField(label="Email Address", required=True)
    phone = forms.CharField(label="Phone Number", max_length=30)
    message = forms.CharField(widget=forms.Textarea, required=False)
