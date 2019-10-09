from django.db import models
from colorful.fields import RGBColorField

from .hub import Hub, HubType
from .membership import Membership
from user.models import CustomUser, Address, Name, Gender


class HubMember(models.Model):

    ''' A container model for information about a member of a Hub. The model contains 'person' level data,
    i.e. name, gender, dob, address etc, it also contains membership models i.e. Rank and HubGroup memberships 
    as well general Hub Memberships. There is a link to CustomUser and as the Hubs will most likely 
    be Schools there is a built-in attribute nsn for a National Student Number. '''

    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, related_name='hub_memberships')

    nsn = models.CharField(max_length=30, blank=True) # national student number

    # >>> hub_roles (HubRoleMembership)
    # >>> ranks (RankHubMembership)
    # >>> hub_groups (HubGroupMembership)

    # >>> tournament_competitors (Competitor)

    # >>> name (HubMemberName)
    dob = models.DateField(null=True)
    gender = models.ForeignKey(Gender, null=True, on_delete=models.SET_NULL)
    # >>> address (HubMemberAddress)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

class HubMemberName(Name):

    ''' Inherits from NameBase and links name values to a HubMember model. '''

    # firstname, middlenames, surname, preferred_name
    member = models.OneToOneField(HubMember, on_delete=models.CASCADE, related_name='name')

class HubMemberAddress(Address):

    ''' Inherits from Address and links the values to a HubMember model'''

    # line1, line2, line3, town_city, postcode, country
    member = models.OneToOneField(HubMember, on_delete=models.CASCADE, related_name='address')



class HubRole(models.Model):

    ''' A singular type of HubRole membership, i.e. Student, Teacher, Staff, Parent, Club Member etc. '''

    hub_type = models.ForeignKey(HubType, null=True, on_delete=models.SET_NULL, related_name='hub_membership_types')

    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)

class HubRoleLink(models.Model):

    pass

class HubRoleMembership(Membership):

    ''' Inherits from Membership and links a HubMembershipType to a HubMember,
    i.e. A HubMember may have Student type membership starting from 01/01/18 - currently, and 
    therefore the membership is active. There is also a membership_id attribute where 
    a student/staff id number can be included. 
    
    HubMembership differs from membership of HubGroups; HubMembership indicates what role/s 
    the person has in the overall Hub, HubGroups indicate which groups in the Hub they belong to 
    i.e. Student is a HubMembership, Kennedy House or 12DB (a form class) are HubGroups. '''
    
    MEMBER_RELATED_NAME = 'hub_roles'

    membership_type = 'HubRole'
    # >>> hub_role_link # shows links between various roles, specifically parent - student - family
    membership = models.ForeignKey(HubRole, null=True, on_delete=models.SET_NULL, related_name='hub_memberships')



class HubGroupType(models.Model):

    ''' '''

    name = models.CharField(max_length=30, unique=True)

class HubGroup(models.Model):

    ''' A group within a Hub such as a House Group, a YearGroup, or even a Class i.e. 13DB. 
    These groups can be semi-permanent, or only for a time period i.e. a Year. 

    HubMembers can have HubGroupMembership which indicates their membership in a HubGroup 
    i.e. a HubGroup is a House called Kennedy, which was started 01/01/74 and is still active. 
    A HubMember had HubGroupMembership to that House for the 5 years they were 
    at that Hub/School. '''

    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='hub_groups')
    type = models.ForeignKey(HubGroupType, null=True, on_delete=models.SET_NULL, related_name='hub_groups')
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    name = models.CharField(max_length=30) 
    description = models.TextField(blank=True, default='')
    
    # >>> competitor_groups
    # >>> 

    colour = RGBColorField(blank=True)
    text_colour = RGBColorField(colors=['#000000', '#ffffff'], blank=True)

class HubGroupMembership(Membership):

    ''' A timed record of membership in a HubGroup, i.e. a HubGroup could be a class like 12PB, 
    a student will not be in that class forever. '''

    MEMBER_RELATED_NAME = 'hub_groups'

    membership_type = 'HubGroup'
    membership = models.ForeignKey(HubGroup, null=True, on_delete=models.CASCADE, related_name='hub_memberships')



class RankHubMembership(Membership):

    ''' A timed record of membership in a Rank, i.e. if the Rank is "School Year - NZ Year 10", 
    a student is not just that Rank forever. '''

    MEMBER_RELATED_NAME = 'ranks'

    membership_type = 'Rank'
    membership = models.ForeignKey(to='tournament.Rank', null=True, on_delete=models.CASCADE, related_name='hub_rank_memberships')