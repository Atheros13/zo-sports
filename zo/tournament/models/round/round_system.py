from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class RoundSystem(models.Model):

	CHOICES_ROUND_SYSTEM_TYPE = {'pk__in':ContentType.objects.all().filter(model__startswith='round system type')} 

	content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE, limit_choices_to=CHOICES_ROUND_SYSTEM_TYPE)
	object_id = models.PositiveIntegerField()
	system = GenericForeignKey('content_type', 'object_id')

class RoundSystemTypeSemiLinear(models.Model):

    pass
