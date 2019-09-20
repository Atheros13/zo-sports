from django.db import models
from django.contrib.postgres.fields import ArrayField

from tournament.models.contest import ContestType
from tournament.models.general import Measurement

class ContestTypeJump(ContestType):

	style = models.CharField(max_length=30, blank=True)

	class Meta:

		abstract = True

class ContestTypeJumpHorizontal(ContestTypeJump):

	pass

class ContestTypeJumpVertical(ContestTypeJump):

	pass
