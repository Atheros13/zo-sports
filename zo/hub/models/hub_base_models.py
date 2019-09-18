from django.db import models

from user.models import CustomUser
from public.models import Address

# Create your models here.

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
    
    permission_admin = models.ManyToManyField(CustomUser, related_name='hub_permission_admin')
    permission_staff = models.ManyToManyField(CustomUser, related_name='hub_permission_staff')
    is_public = models.BooleanField(default=False)

    ### IN OneToOne ATTRIBUTES
    # address

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