from django.db import models
from django.contrib.postgres.fields import ArrayField

from tournament.models.contest import ContestType
from tournament.models.general import ApparatusThrow
from tournament.models.score import ScoredByMeasurement

class ContestTypeThrow(ContestType):

	style = models.CharField(max_length=30, blank=True)
	apparatus = models.ForeignKey(ApparatusThrow, null=True,
									on_delete=models.SET_NULL)

    scored_by = models.ForeignKey(ScoredByMeasurement, null=True, on_delete=models.SET_NULL)