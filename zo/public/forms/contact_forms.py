from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, BadHeaderError

from hub.models import HubUserSignup
from user.models import CustomUser, UserSignup

class UserSignUpContactForm(forms.ModelForm):

    title = 'Sign Up'
    description = 'Click to sign up as an authenticated user.'

    class Meta:
        model = UserSignup
        fields = ['firstname', 'surname', 'phone', 'email', 'message']

    def process_contact(self, *args, **kwargs):

        model = self.save(commit=False)

        # checks if 
        if CustomUser.objects.filter(email=model.email) or UserSignup.objects.filter(email=model.email) or HubUserSignup.objects.filter(email=model.email):
            return False, 'error message'

        model.save()
        email_message = 'User Only Signup\n\n'
        email_message += 'https://112.109.84.57:8000/user/confirm_signup'

        send_mail('User Signup', email_message, model.email, ['info@zo-sports.com'])

        return True, ''

class HubUserSignUpContactForm(forms.ModelForm):

    class Meta():
        model = HubUserSignup
        fields = ['hub_type', 'hub_name', 'hub_phone', 'hub_address', 'hub_towncity',
                  'firstname', 'surname', 'phone', 'email',
                  'message']

    def process_contact(self, *args, **kwargs):

        model = self.save(commit=False)

        # checks if 
        if CustomUser.objects.filter(email=model.email) or UserSignup.objects.filter(email=model.email) or HubUserSignup.objects.filter(email=model.email):
            return False, 'error message'

        model.save()
        email_message = 'User & Hub Signup\n\n'
        email_message += 'https://112.109.84.57:8000/user/confirm_signup'

        return True, ''


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

        return True, 'error message'

