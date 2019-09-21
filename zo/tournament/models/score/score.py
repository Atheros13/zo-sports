from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from tournament.models.general.measurement import *

class ScoredBy(models.Model):

    name = models.CharField(max_length=30)

    class Meta:

        abstract = True

    def __str__(self):

        return self.name

class ScoredByScoringSystem(ScoredBy):

    ''' This is a theoretical class at the moment. It would be used to 
    score contests that have a set scoring system i.e. Rugby, Tennis etc. '''

    class Meta:

        abstract = True

class ScoredByMeasurement(ScoredBy):

    ''' Contest results are scored based on what measurement value a 
    Competitor gets i.e. if the measurement_type is Time and the 
    best_is_highest_value == False, the Contest is scored by comparing 
    Time values of Competitors with the lowest values being the better results. '''

    measurement_type = models.ForeignKey(MeasurementType, on_delete=models.CASCADE)
    best_is_highest_value = models.BooleanField()

class ScoredByMeasurementAttempts(ScoredByMeasurement):

    pass

