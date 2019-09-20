from django.db import models
from django.contrib.postgres.fields import ArrayField

class Apparatus(models.Model):

	name = models.CharField(max_length=30)

	class Meta:

		abstract = True

class ApparatusThrow(Apparatus):

	pass

