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

    CHOICES_CONTACT_TYPE = [
        ('General', 'General'), ('Signup', 'Signup'),
        ('Technical', 'Technical')
        ]

    contact_type = forms.ChoiceField(label='Subject',
                                   choices=CHOICES_CONTACT_TYPE,
                                   widget=forms.RadioSelect)
    firstname = forms.CharField(label="First Name", max_length=50, required=True)
    surname = forms.CharField(label="Surname", max_length=50, required=True)
    email = forms.EmailField(label="Email Address", required=True)
    phone = forms.CharField(label="Phone Number", max_length=30, required=False)
    message = forms.CharField(label='Message', widget=forms.Textarea(), required=False)

class EmailForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput({
                                   'class': 'form-control',
                                   'placeholder': 'Email'}))