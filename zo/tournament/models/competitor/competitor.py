from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from colorful.fields import RGBColorField

from .competitor_group import *
from hub.models import Hub, HubGroup
from tournament.models.tournament import Tournament
from tournament.models.grade import Rank
from user.models import CustomUser, NameBase, Gender

class Competitor(models.Model):

    ''' '''

    tournament = models.ForeignKey(Tournament, null=True, on_delete=models.CASCADE,
                                   related_name='competitors')
    competitor_group = models.ForeignKey(CompetitorGroup, null=True, 
                                         on_delete=models.SET_NULL,
                                         related_name='competitors')

    # >>> name
    dob = models.DateField(null=True)
    gender = models.ForeignKey(Gender, null=True,
                               on_delete=models.SET_NULL)
    ranks = models.ManyToManyField(Rank)

    hub_groups = models.ManyToManyField(HubGroup, related_name='competitors')
    hub_member = models.ForeignKey(to="hub.HubMember", null=True,
                                   on_delete=models.SET_NULL,
                                   related_name='competitor_tournaments')
    custom_user = models.ForeignKey(CustomUser, null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='competitor_tournaments')

    is_team = models.BooleanField(default=False)
    team_name = models.CharField(max_length=30, blank=True)
    competitors = models.ManyToManyField('self', related_name='competitor_teams')

    def __str__(self):
        if self.is_team:
            return self.team_name
        return self.name.__str__()

class CompetitorName(NameBase):

    ''' A NameBase inherited model, for use with a Competitor. '''

    # firstname, middlename, surname, preferred name
    competitor = models.OneToOneField(Competitor, on_delete=models.CASCADE,
                                       related_name='name')
