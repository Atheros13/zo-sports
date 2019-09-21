from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from colorful.fields import RGBColorField

from .competitor_group import *
from hub.models import Hub, HubGroup
from tournament.models.tournament import Tournament
from tournament.models.grade import Rank
from user.models import CustomUser, NameBase, Gender

class Participant(models.Model):

    tournament = models.ForeignKey(Tournament, null=True, on_delete=models.CASCADE,
                                   related_name='participants')

    dob = models.DateField()
    gender = models.ForeignKey(Gender, null=True,
                               on_delete=models.SET_NULL)
    ranks = models.ManyToManyField(Rank)
    hub_groups = models.ManyToManyField(HubGroup, related_name='participants')

    custom_user = models.ForeignKey(CustomUser, null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='tournament_participations')

    def __str__(self):
        return self.name.__str__()

class ParticipantName(NameBase):

    ''' A NameBase inherited model, for use with a Participant. '''

    participant = models.OneToOneField(Participant, on_delete=models.CASCADE,
                                       related_name='name')

class Competitor(models.Model):

    ''' '''

    competitor_group = models.ForeignKey(CompetitorGroup, null=True, 
                                         on_delete=models.SET_NULL,
                                         related_name='competitors')
    participant = models.OneToOneField(Participant, null=True, on_delete=models.CASCADE, 
                                    related_name='competitor')
    tournament = models.ForeignKey(Tournament, null=True, on_delete=models.CASCADE,
                                   related_name='competitors')

    is_team = models.BooleanField(default=False)
    name = models.CharField(max_length=30, blank=True)
    participants = models.ManyToManyField(Participant, related_name='competitor_teams')

    def __str__(self):
        if self.is_team:
            return self.name
        return self.participant.__str__()
