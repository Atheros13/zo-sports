from django.db import models
from colorful.fields import RGBColorField

from .membership import Membership
from user.models import CustomUser
from public.models import Address

class HubType(models.Model):
    
    type = models.CharField(max_length=30, unique=True)
    #super_type = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='sub_types')

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


class HubGroupType(models.Model):

    ''' '''

    name = models.CharField(max_length=30, unique=True)

class HubGroup(Membership):

    ''' A group within a Hub. Unlike a HubMembership, this is more internal; a House Group, 
    a YearGroup, or even a Class i.e. 13DB. These groups can be semi-permanent, or only for a 
    time period i.e. a Year. HubMembers can have HubGroupMembership which indicates their 
    membership in a HubGroup i.e. a HubGroup is a House called Kennedy, which was started 01/01/74 
    and is still active. A HubMember had HubGroupMembership to that House for the 5 years they were 
    at that Hub/School. '''

    # start_date, end_date, is_active, auto_end_membership
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='hub_groups')
    type = models.ForeignKey(HubGroupType, null=True, on_delete=models.SET_NULL, related_name='hub_groups')

    name = models.CharField(max_length=30) 
    description = models.TextField(blank=True, default='')
    
    # >>> competitor_groups
    # >>> 

    colour = RGBColorField(blank=True)
    text_colour = RGBColorField(colors=['#000000', '#ffffff'], blank=True)


class HubSignUp(models.Model):

    hub_type = models.ForeignKey(HubType, null=True, on_delete=models.SET_NULL, verbose_name='Hub Type')
    name = models.CharField(verbose_name='Hub Name', max_length=30)
    phone = models.CharField(verbose_name='Hub Phone', max_length=30, blank=True)
    email = models.EmailField(verbose_name='Hub Email', blank=True)
    town_city = models.CharField(verbose_name='Town/City', max_length=30)
    
    requester = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
