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

class ScoredByMeasurement(ScoredBy):

    measurement_type = models.ForeignKey(MeasurementType, null=True, on_delete=models.CASCADE)
    measurement_qualifier = models.CharField(max_length=30, blank=True)

class ScoredByMeasurementAttempts(ScoredByMeasurement):

    pass


