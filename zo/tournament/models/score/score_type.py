from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from tournament.models.general.measurement import *
from tournament.models.competitor import Competitor
from tournament.models.round import ContestInstance

class Score(models.Model):

    ''' A singular scoring unit by a Competitor in a ContestInstance. '''

    CHOICES_SCORE_TYPE = {'pk__in':ContentType.objects.all().filter(model__startswith='score type')} 

    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE, limit_choices_to=CHOICES_SCORE_TYPE)
    object_id = models.PositiveIntegerField()

    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='scores')
    score = GenericForeignKey('content_type', 'object_id')
    contest_instance = models.ForeignKey(ContestInstance, on_delete=models.CASCADE, related_name='scores')

    
class ScoreTypeMeasurement(models.Model):

    # >>> measurement
    participation = models.BooleanField(default=False)
    placing = models.PositiveIntegerField(blank=True)

class ScoreMeasurement(Measurement):

    measurement = models.OneToOneField(ScoreTypeMeasurement, on_delete=models.CASCADE, related_name='measurement')

class ScoreTypeMeasurementAttempts(ScoreTypeMeasurement):

    pass
