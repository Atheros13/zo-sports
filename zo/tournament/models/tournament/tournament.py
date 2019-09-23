from django.db import models

from hub.models import Hub
from user.models import CustomUser
from tournament.models.activity import Activity
from tournament.models.competitor.competitor_group import CompetitorGroup
from tournament.models.contest import Contest
from tournament.models.grade import Grade
from tournament.models.event import Event

class TournamentStone(models.Model):

    name = models.CharField(max_length=50)

class TournamentName(models.Model):

    tournament = models.OneToOneField('Tournament', on_delete=models.CASCADE,
                                      related_name='name')

class Tournament(models.Model):

    ''' The central model which connects all other tournament models. This connects 
    what the tournament does, who runs it, who is competing, what they are competing in,
    how they are competing, how they are scored and how those scores and assign point value, 
    it records entries, results, and everything to do with the tournament.
    
    Many other models ForeignKey direct to this model, as such they do not appear in the 
    stated attributes (they are reverse related). '''

    activity = models.ForeignKey(Activity, null=True, on_delete=models.CASCADE, related_name='tournaments')

    created_on = models.DateField(null=True)
    created_by = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL,
                                   related_name='tournaments_created_by')
    #admins
    hubs = models.ManyToManyField(Hub, related_name='tournaments')

    competitor_groups = models.ManyToManyField(CompetitorGroup, related_name='tournaments')
    # <<< participants 
    # <<< competitors 

    # <<< events
    contests = models.ManyToManyField(Contest, related_name='tournaments')
    grades = models.ManyToManyField(Grade, related_name='tournaments')



class TournamentEvent(models.Model):

    name = models.CharField(max_length=30, blank=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE,
                                   related_name='events')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, 
                              related_name='tournament_events')

    def __str__(self):
        if self.name:
            return self.name
        return self.event.__str__(tournament)

