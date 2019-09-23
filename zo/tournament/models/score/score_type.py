from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from tournament.models.general.measurement import Measurement
from tournament.models.competitor import Competitor
from tournament.models.contest.contest_instance import ContestInstance, ContestMeasurementAttempt

class Score(models.Model):

    ''' A singular scoring unit by a Competitor in a ContestInstance. 
	A Score has three "values" associated with it, a Participation value which determines if the 
	Competitor entered but did not compete, a Placing value which is determined based on 
	comparing different Scores in a ContestInstance, and the self.score value itself, which is 
	a ContentType/GenericForeignKey relationship to one of the many different ScoreType models. '''

    CHOICES_SCORE_TYPE = {'pk__in':ContentType.objects.all().filter(model__startswith='score type')} 

    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE, limit_choices_to=CHOICES_SCORE_TYPE)
    object_id = models.PositiveIntegerField()

    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='scores') # who
    contest_instance = models.ForeignKey(ContestInstance, on_delete=models.CASCADE, related_name='scores') # where
    
    participation = models.BooleanField(default=False)
    placing = models.PositiveIntegerField(blank=True)
    score = GenericForeignKey('content_type', 'object_id') # what
    
###
    
class ScoreTypeMeasurementRace(models.Model):

	''' ScoreType which contains a single ScoreMeasurementRace measurement,
	used for contests such as 100m sprint or 50m butterfly swim, where a competitor has 
	one measurment, in one ContestInstance, and may or may not be in a lane'''

    # >>> measurement
	lane = models.PositiveIntegerField(blank=True)
	score = GenericRelation()

class ScoreMeasurementRace(Measurement):

    ''' This model inherits from the Measurement model and adds a link to the 
    ScoreTypeMeasurementRace model. '''
    
    # value & unit
    score_type = models.OneToOneField(ScoreTypeMeasurementRace, on_delete=models.CASCADE, related_name='measurement')

###

class ScoreTypeMeasurementDistance(models.Model):

	''' ScoreType which contains multiple ScoreMeasurementDistance measurements, 
	used for contests such as Long Jump or Discus, where a competitor has 
	multiple measurements in one ContestInstance. '''

	# >>> measurements
	score = GenericRelation()

class ScoreMeasurementDistance(Measurement):

	# value & unit
	no_value = models.BooleanField(default=False)
	order = models.PositiveIntegerField()
	score_type = models.ForeignKey(ScoreTypeMeasurementDistance, on_delete=models.CASCADE, related_name='measurements')

###

class ScoreTypeAttempts(models.Model):

	''' ScoreType where the ContestInstance establishes the measurement which is attempted. 
	This model records what the competitor did or achieved at each attempt, used for 
	contests such as High Jump or Pole Vault. '''

	# >>> attempts
	score = GenericRelation()

class ScoreAttempt(models.Model):  
    ''' This model records the multiple results achieved at a singular contest_measurement 
	i.e. if the High Jump measurement is 1.6m, this model will record the results for the
	three attempts at that height (through the self.results queryset). '''
    # >>> results
    	
	score_type = models.ForeignKey(ScoreTypeAttempts, on_delete=models.CASCADE, related_name='attempts')
	contest_measurement = models.ForeignKey(ContestMeasurementAttempt, on_delete=models.CASCADE, related_name='score_attempts')


class ScoreAttemptResult(models.Model):

	''' This model is a singular result for a ScoreAttempt. It has an order attribute i.e. first, second, third attempt,
	as well as the result which could be Yes (successful), No (failed), Pass (passed), N/A (when a earlier attempt was
	successful) and "" (blank, when no attempt has been made yet. '''

	CHOICES = [('Yes', 'Yes'), ('No', 'No'), 
			('Pass', 'Pass'), ('N/A', 'N/A'), ('', '')]

	order = models.PositiveIntegerField()
	result = models.CharField(max_length=10, choices=CHOICES, blank=True)
	score_attempt = models.ForeignKey(ScoreAttempt, on_delete=models.CASCADE, related_name='results')



