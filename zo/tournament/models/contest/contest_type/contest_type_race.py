from django.db import models

from tournament.models.contest import ContestType
from tournament.models.general import Measurement, ObstacleRace
from tournament.models.score import ScoredByMeasurement

class ContestTypeRace(ContestType):

	distance = models.ForeignKey(Measurement, null=True, on_delete=models.SET_NULL)
	style = models.CharField(max_length=30, blank=True)

    scored_by = models.ForeignKey(ScoredByMeasurement, null=True, on_delete=models.SET_NULL)

	class Meta:

		abstract = True

	def __str__(self):
		name = "%s " % self.distance.short_name()
		if self.style != '':
			name += self.style
		return name.rstrip()

class ContestTypeRaceRunning(ContestTypeRace):

	surface = models.CharField(max_length=30, blank=True)

	obstacle = models.ForeignKey(ObstacleRace, null=True,
									on_delete=models.SET_NULL)

class ContestTypeRaceSwimming(ContestTypeRace):

	water = models.CharField(max_length=30, blank=True)
	pool_length = models.ForeignKey(Measurement, null=True, on_delete=models.SET_NULL,
                                    related_name='swimming_pool_length')
