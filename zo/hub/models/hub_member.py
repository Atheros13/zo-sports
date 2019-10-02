from django.db import models

from .hub import Hub, HubGroup, HubType
from .membership import Membership
from public.models import Address
from user.models import CustomUser, NameBase, Gender
from tournament.models import Rank


class HubMember(models.Model):

    ''' A container model for information about a member of a Hub. The model contains 'person' level data,
    i.e. name, gender, dob, address etc, it also contains membership models i.e. Rank and HubGroup memberships 
    as well general Hub Memberships. There is a link to CustomUser and as the Hubs will most likely 
    be Schools there is a built-in attribute nsn for a National Student Number. '''

    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, related_name='hub_memberships')

    nsn = models.CharField(max_length=30, blank=True) # national student number

    # >>> memberships (HubMembership)
    # >>> ranks (RankHubMembership)
    # >>> hub_groups (HubGroupMembership)

    # >>> tournament_competitors (Competitor)

    # >>> name (HubMemberName)
    dob = models.DateField(null=True)
    gender = models.ForeignKey(Gender, null=True, on_delete=models.SET_NULL)
    # >>> address (HubMemberAddress)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)



class HubMembershipType(models.Model):

    ''' A singular type of Hub membership, i.e. Student, Teacher, Staff, Parent, Club Member etc. '''

    hub_type = models.ForeignKey(HubType, null=True, on_delete=models.SET_NULL, related_name='hub_membership_types')
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)

class HubMembership(Membership):

    ''' Inherits from Membership and links a HubMembershipType to a HubMember,
    i.e. A HubMember may have Student type membership starting from 01/01/18 - currently, and 
    therefore the membership is active. There is also a membership_id attribute where 
    a student/staff id number can be included. 
    
    HubMembership differs from membership of HubGroups; HubMembership indicates what role/s 
    the person has in the overall Hub, HubGroups indicate which groups in the Hub they belong to 
    i.e. Student is a HubMembership, Kennedy House or 12DB (a form class) are HubGroups. '''
    
    # start_date, end_date, auto_end, is_active
    type = models.ForeignKey(HubMembershipType, on_delete=models.CASCADE)
    member = models.ForeignKey(HubMember, on_delete=models.CASCADE, related_name='memberships')
    membership_id = models.CharField(max_length=50, blank=True)

class HubMemberName(NameBase):

    ''' Inherits from NameBase and links name values to a HubMember model. '''

    # firstname, middlenames, surname, preferred_name
    member = models.OneToOneField(HubMember, on_delete=models.CASCADE, related_name='name')

class HubMemberAddress(Address):

    ''' Inherits from Address and links the values to a HubMember model'''

    # line1, line2, line3, town_city, postcode, country
    member = models.OneToOneField(HubMember, on_delete=models.CASCADE, related_name='address')



class RankHubMembership(Membership):

    ''' A timed record of membership in a Rank, i.e. if the Rank is "School Year - NZ Year 10", 
    a student is not just that Rank forever. '''

    # start_date, end_date, is_active
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
    member = models.ForeignKey(HubMember, on_delete=models.CASCADE, related_name='ranks')

class HubGroupMembership(Membership):

    ''' A timed record of membership in a HubGroup, i.e. a HubGroup could be a class like 12PB, 
    a student will not be in that class forever. '''

    # start_date, end_date, is_active
    hub_group = models.ForeignKey(HubGroup, on_delete=models.CASCADE)
    member = models.ForeignKey(HubMember, on_delete=models.CASCADE, related_name='hub_groups')