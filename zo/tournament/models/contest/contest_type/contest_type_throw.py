from django.db import models
from django.contrib.postgres.fields import ArrayField

from tournament.models.contest import ContestType
from tournament.models.general import ApparatusThrow

class ContestTypeThrow(ContestType):

	style = models.CharField(max_length=30, blank=True)
	apparatus = models.ForeignKey(ApparatusThrow, null=True,
									on_delete=models.SET_NULL)

