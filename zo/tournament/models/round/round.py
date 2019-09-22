from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from tournament.models.tournament import TournamentEvent
from .round_system import RoundSystem

class RoundController(models.Model):

    ''' This model controls how the rounds in a TournamentEvent are put together. The way it puts 
    Rounds together is based on which RoundSystem it uses. There is always 1 primary_round_node, 
    which is then linked to the remaining rounds (as per the RoundSystem). '''

    # >>> primary_round_node
    event = models.OneToOneField(TournamentEvent, on_delete=models.CASCADE, related_name='round_controller')
    round_system = models.ForeignKey(RoundSystem, null=True, on_delete=models.SET_NULL, related_name='round_controllers')
    


class Round(models.Model):

    ''' A Round is a container for either other Round objects or ContestInstance objects.
    If a round is deleted, all sub_rounds, next_rounds, and contest_instances are also deleted. 
    Due to how Django model relationships work, Rounds point backwards to previous rounds, 
    or outwards to container rounds. '''

    name = models.CharField(max_length=30, blank= True)
    round_controller = models.OneToOneField(RoundController, null=True, on_delete=models.CASCADE, related_name='primary_round')

    # >>> contest_instances

    # >>> sub_rounds
    container_round = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_rounds')
    
    # >>> next_rounds
    previous_round = models.ForeignKey('self', on_delete=models.CASCADE, related_name='next_rounds')


class ContestInstance(models.Model):

    ''' A singular instance of a Contest. Score objects that contain the scores for each Competitor
    have a reverse relationship to ContestInstance. Depending on the type of Contest, there may be 
    other reverse relationship objects i.e. RaceLanes, though these might be part of a more complex 
    additional construct. '''

    name = models.CharField(max_length=30, blank=True)
    # >>> scores
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='contest_instances')
    

