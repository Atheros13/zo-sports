
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, BadHeaderError

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

class GeneralContactForm(forms.Form):

    title = 'General'
    description = 'Click to send a general message'

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
        
        subject = '%s Contact' % self.contact_type

        message = ''
        if f['phone']:
            message += 'Phone: %s\n\n' % f['phone']
        message += f['message']
        
        send_mail(subject, message, email, ['info@zo-sports.com'])

class TechnicalContactForm(GeneralContactForm):

    title = 'Technical'
    description = 'Click for technical issues, please include as much information as possible'
