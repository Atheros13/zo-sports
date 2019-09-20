from django.db import models

from tournament.models.general import Measurement

class Obstacle(models.Model):

	name = models.CharField(max_length=30)
	
	#measure = models.CharField(max_length=30, blank=True) # i.e. height, length etc ???
	measurement = models.ForeignKey(Measurement, null=True,
									on_delete=models.SET_NULL)

	class Meta:

		abstract = True

	def __str__(self):
		if self.measurement != None:
			return '%s %s' % (self.name, self.measurement.short_name())
		return self.name

class ObstacleRace(Obstacle):

	pass
