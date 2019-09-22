from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from tournament.models.tournament import TournamentEvent
from .round import Round

class ContestInstance(models.Model):

    '''  '''
    CHOICES_CONTEST_INSTANCE_TYPE = {'pk__in':ContentType.objects.all().filter(model__startswith='contest instance type')} 

    name = models.CharField(max_length=30, blank=True)
    round = models.ForeignKey(Round, on_delete=models.CASCADE, 
                              related_name='contest_instances')

    content_type = models.ForeignKey(ContentType, 
                                     null=True, on_delete=models.CASCADE,
                                     limit_choices_to=CHOICES_CONTEST_INSTANCE_TYPE)
    object_id = models.PositiveIntegerField()
    instance = GenericForeignKey('content_type', 'object_id')
    

class ContestInstanceType(models.Model):

    pass

    class Meta:

        abstract = True


class ContestInstanceTypeMeasurement(ContestInstanceType):

    pass


class ContestInstanceTypeMeasurementAttempts(ContestInstanceType):

    pass