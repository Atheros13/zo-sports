from django import forms
from hub.models import HubSignUp
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail, BadHeaderError

class HubSignUpContactForm(forms.ModelForm):

    title = 'Create Hub'
    description = "Click to request to create a new Hub, i.e. a School, Club etc. Please make sure the Hub doesn't already exist."

    class Meta:
        model = HubSignUp
        fields = ['hub_type', 'name', 'phone', 'email', 'town_city']

    def process_contact(self, user=None):
        
        model = self.save(commit=False)
        model.requester = user
        model.save()

        message = '%s %s %s %s %s' % (model.hub_type, model.name, model.phone, model.email, model.town_city)
        message += '\n%s' % model.id
        message += '\n%s' % user.id

        send_mail('Hub Signup', message, user.email, ['info@zo-sports.com'])
