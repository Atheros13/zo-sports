from django.db import models

class MeasurementType(models.Model):
    
    ''' Specifies what the MeasurementUnitGroup measures i.e. Time, Distance, Volume etc
    for example, the Metric System that measures Distance is different from the Metric 
    system that measures Volume, as well as the Imperial System that measures Distance. '''
    
    type = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.type

class MeasurementUnit(models.Model):

	measurement_group = models.ForeignKey('MeasurementUnitGroup',
											on_delete=models.CASCADE,
											related_name='units')

	name = models.CharField(max_length=20)
	short_name = models.CharField(max_length=10)
	rank_value = models.PositiveIntegerField()

	def __str__(self):
		return self.name

class MeasurementUnitGroup(models.Model):

	measurement_type = models.ForeignKey(MeasurementType, null=True, on_delete=models.SET_NULL)
	name = models.CharField(max_length=30)
	description = models.TextField()

	def __str__(self):
		return self.name

	def add_unit(self, name, symbol, rank_value=None, highest=False, lowest=False):

		if rank_value != None:
			if self.units.filter(rank_value=rank_value):
				return 'A MeasurementUnit already has the rank_value of %s' % rank_value
		elif highest:
			h = self.units.all().order_by('-rank_value')
			if h:
				rank_value = h[0].rank_value + 1
			else:
				rank_value = 1
		elif lowest:
			l = self.units.all().order_by('rank_value')
			if l:
				if l[0].rank_value == 1:
					for unit in l:
						unit.rank_value += 1
						unit.save()
				rank_value = 1
			else:
				rank_value = 1				
		else:
			return False

		MeasurementUnit(name=name, symbol=symbol, rank_value=rank_value).save()
		return True

class Measurement(models.Model):

	value = models.PositiveIntegerField()
	unit = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE,
								related_name='measurements')

	def __str__(self):
		return '%s %s' % (self.value, self.unit.name)

	def short_name(self):
		return '%s %s' % (self.value, self.unit.short_name)
