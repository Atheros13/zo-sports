from django.db import models
from colorful.fields import RGBColorField
from djangoyearlessdate.models import YearlessDateField

from user.models import CustomUser, Address

### 

class HubGenderType(models.Model):

    name = models.CharField(max_length=30)
    #gender = 

class HubType(models.Model):

    CHOICES = [('School', 'School'), ('Club', 'Club'), ('Organisation', 'Organisation')]
    
    type = models.CharField(max_length=30, choices=CHOICES)

    gender_type = models.ForeignKey(HubGenderType, null=True, on_delete=models.SET_NULL, related_name='hub_types')
    grade_type = models.CharField(max_length=30)

    def __str__(self):
        return self.type

class Hub(models.Model):

    hub_type = models.ForeignKey(HubType, verbose_name='Hub Type', null=True, on_delete=models.SET_NULL)
    
    #hub_year_start = YearlessDateField(null=True)
    
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    
    main_contact = models.ForeignKey(CustomUser, related_name='hub_main_contact', 
                                     on_delete=models.SET_NULL, null=True)
    
    permission_admin = models.ManyToManyField(CustomUser, related_name='hub_admin')
    is_public = models.BooleanField(default=False)

    class Meta:

        pass

    def __str__(self):
        return self.name

    ### PERMISSION FUNCTIONS ###

    def has_admin(self, user):
        if user in permission_admin or user == main_contact:	
            return True

class HubAddress(Address):

    ''' Inherits from the Address model and links to a Hub ''' 

    hub = models.OneToOneField(Hub, on_delete=models.CASCADE, related_name='address')

###

class HubSignUp(models.Model):

    hub_type = models.ForeignKey(HubType, null=True, on_delete=models.SET_NULL, verbose_name='Hub Type')
    name = models.CharField(verbose_name='Hub Name', max_length=30)
    phone = models.CharField(verbose_name='Hub Phone', max_length=30, blank=True)
    email = models.EmailField(verbose_name='Hub Email', blank=True)
    town_city = models.CharField(verbose_name='Town/City', max_length=30)
    
    requester = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
