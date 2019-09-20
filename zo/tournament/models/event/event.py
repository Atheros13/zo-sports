from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from tournament.models.contest import Contest
from tournament.models.grade import Grade
from tournament.models.tournament import Tournament

class Event(models.Model):

    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='events')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='events')

class EventName(models.Model):

    name = models.CharField(max_length=30)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='name')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, 
                                   related_name='event_name')