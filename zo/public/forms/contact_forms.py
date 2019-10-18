from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, BadHeaderError

from hub.models import Hub
from user.models import CustomUser, UserSignup

class UserSignUpContactForm(forms.ModelForm):

    title = 'Sign Up'
    description = 'Click to sign up as an authenticated user.'

    class Meta:
        model = UserSignup
        fields = ['firstname', 'surname', 'phone', 'email', 'message']

    def process_contact(self, *args, **kwargs):

        model = self.save(commit=False)

        if CustomUser.objects.filter(email=model.email) or UserSignup.objects.filter(email=model.email):
            return False

        model.save()
        email_message = 'Name: %s %s\n' % (model.firstname, model.surname)
        email_message += 'Email: %s\nPhone: %s\n' % (model.email, model.phone)
        email_message += 'Message: %s\n\n' % model.message
        email_message += 'https://112.109.84.57:8000/user/confirm_user_signup/%s' % model.id

        send_mail('User Signup', email_message, model.email, ['info@zo-sports.com'])

        return True

class HubUserSignUpContactForm(forms.ModelForm):

    title = 'Sign Up & Hub'
    description = '''Click to sign up as an authenticated user, 
                    and to also request the creation of a new Hub.'''

    hub_name = forms.CharField(label='Hub Name', max_length=30, required=True)
    hub_phone = forms.CharField(label='Hub Phone Number', max_length=30)
    hub_address = forms.CharField(label='Hub Street Address', max_length=30)
    hub_towncity = forms.CharField(label='Hub Town/City', max_length=30)
    user_firstname = forms.CharField(label='User Firstname', max_length=30)
    user_surname = forms.CharField(label='User Surname', max_length=30)
    user_phone = forms.CharField(label='User Phone Number', max_length=30)
    user_email = forms.EmailField(label='User Email')
    message = forms.CharField(label='Message', widget=forms.Textarea())

    class Meta():
        model = Hub
        fields = ['hub_type', 'hub_name', 'hub_phone', 'hub_address', 'hub_towncity',
                  'user_firstname', 'user_surname', 'user_phone', 'user_email',
                  'message']

    def process_contact(self, *args, **kwargs):

        return True

class GeneralContactForm(forms.Form):

    title = 'General'
    description = 'Click to send a general message'

    name = forms.CharField(label='Name', max_length=30, required=True)
    email = forms.EmailField(label="Email Address", required=True)
    phone = forms.CharField(label="Phone Number", max_length=30, required=False)
    message = forms.CharField(label='Message', widget=forms.Textarea(), required=True)

    def process_contact(self, user=False, hub=False, tournament=False):
        
        f = self.cleaned_data

        email = 'none@none.com'
        if f['email']:
            email = f['email']
        elif user:
            email = user.email
        
        subject = '%s Contact' % self.title

        message = 'Name: %s\n' % f['name']
        if f['phone']:
            message += 'Phone: %s\n\n' % f['phone']
        message += f['message']
        
        send_mail(subject, message, email, ['info@zo-sports.com'])

        return True

class TechnicalContactForm(GeneralContactForm):

    title = 'Technical'
    description = 'Click for technical issues, please include as much information as possible'
