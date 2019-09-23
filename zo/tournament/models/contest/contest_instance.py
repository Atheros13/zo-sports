from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from tournament.models.round import Round

class ContestInstance(models.Model):

    '''  '''
    CHOICES_CONTEST_INSTANCE_TYPE = {'pk__in':ContentType.objects.all().filter(model__startswith='contest instance type')} 

    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE, limit_choices_to=CHOICES_CONTEST_INSTANCE_TYPE)
    object_id = models.PositiveIntegerField()

    name = models.CharField(max_length=30, blank=True)
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='contest_instances')
    instance = GenericForeignKey('content_type', 'object_id')
    

class ContestInstanceType(models.Model):

    pass

    class Meta:

        abstract = True



class ContestInstanceTypeMeasurement(ContestInstanceType):

	''' A basic ContestInstance containing Score objects which 
	contain the appropriate measurement value or values of a Competitor. '''

	# >>> scores
	pass


class ContestInstanceTypeMeasurementAttempts(ContestInstanceType):

	# >>> attempts
	# >>> scores
    pass


class ContestMeasurementAttempt(Measurement):

	''' Reverse related to a ContestInstanceTypeMeasurementAttempts object,
	contains value and unit attributes (inherited from Measurement) and also 
	has an order attribute which indicates which order the attempt was 
	done in. Appropriate ScoreTypes will also reverse related to this class. '''

	# value & unit
	# >>> score_attempts ScoreTypeAttempt
	order = models.PositiveIntegerField()
	contest_instance = models.ForeignKey(ContestInstanceTypeMeasurementAttempts, 
											on_delete=models.CASCADE,
											related_name='attempts')

