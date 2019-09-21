from django.db import models
from colorful.fields import RGBColorField

from user.models import CustomUser
from public.models import Address

class HubType(models.Model):
    
    type = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.type

class Hub(models.Model):

    hub_type = models.ForeignKey(HubType, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    
    main_contact = models.ForeignKey(CustomUser, related_name='hub_main_contact', 
                                     on_delete=models.SET_NULL, null=True)
    
    permission_admin = models.ManyToManyField(CustomUser, related_name='hub_admin')
    permission_staff = models.ManyToManyField(CustomUser, related_name='hub_staff')
    is_public = models.BooleanField(default=False)

    class Meta:

        pass

    def __str__(self):
        return self.name

    ### PERMISSION FUNCTIONS ###

    def has_admin(self, user):
        if user in permission_admin or user == main_contact:	
            return True

    def has_staff(self, user):
        if user in permission_staff or user == main_contact or user in permission_admin:
            return True

class HubAddress(Address):

    ''' A wrapper for the Address object so that it can be linked to a Hub ''' 

    hub = models.OneToOneField(Hub, on_delete=models.CASCADE, related_name='address')


class HubGroupType(models.Model):

    name = models.CharField(max_length=30, unique=True)

class HubGroup(models.Model):

    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='hub_groups')
    type = models.ForeignKey(HubGroupType, null=True, on_delete=models.SET_NULL, related_name='hub_groups')
    
    name = models.CharField(max_length=30) 
    description = models.TextField()
    colour = RGBColorField(blank=True)
    text_colour = RGBColorField(colors=['#000000', '#ffffff'], blank=True)