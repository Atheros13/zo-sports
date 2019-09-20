from django.db import models
from django.contrib.postgres.fields import ArrayField

from tournament.models.contest import ContestType
from tournament.models.general import Measurement
from tournament.models.score import ScoredByMeasurement

class ContestTypeJump(ContestType):

	style = models.CharField(max_length=30, blank=True)
    scored_by = models.ForeignKey(ScoredByMeasurement, null=True, on_delete=models.SET_NULL)

	class Meta:

		abstract = True

class ContestTypeJumpHorizontal(ContestTypeJump):

	pass

class ContestTypeJumpVertical(ContestTypeJump):

    scored_by = models.ForeignKey(ScoredByMeasurementAttempts, null=True, on_delete=models.SET_NULL)
