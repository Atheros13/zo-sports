from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from colorful.fields import RGBColorField

from hub.models import Hub, HubGroup

class CompetitorGroupType(models.Model):

    ''' Represents the group types that are competing against 
    each other, i.e. Houses, Schools, Clubs. '''

    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()

class CompetitorGroup(models.Model):

    ''' A Hub, Hubs or HubGroup i.e. a School, a group of Schools in a district,
    or a House at a School. '''

    name = models.CharField(max_length=30)
    description = models.TextField()

    type = models.ForeignKey(CompetitorGroupType, null=True, 
                             on_delete=models.SET_NULL, 
                             related_name='competitor_groups')

    is_hub = models.BooleanField(default=False)
    hubs = models.ManyToManyField(Hub, related_name='competitor_groups')

    is_hub_group = models.BooleanField(default=False)
    hub_groups = models.ManyToManyField(HubGroup, related_name='competitor_groups')
    
    colour = RGBColorField()
    text_colour = RGBColorField(colors=['#000000', '#ffffff'])
