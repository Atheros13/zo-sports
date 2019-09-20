from django.db import models

from tournament.models.general.measurement import *
from .scoring_system import *

class ScoredBy(models.Model):

    scoring_system = models.ForeignKey(ScoringSystem, null=True, on_delete=models.CASCADE)
    measurement_type = models.ForeignKey(MeasurementType, null=True, on_delete=models.CASCADE)
    measurement_qualifier = models.CharField(max_length=30, blank=True)
