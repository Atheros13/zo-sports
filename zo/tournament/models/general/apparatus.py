from django.db import models

class Apparatus(models.Model):

	name = models.CharField(max_length=30)

	class Meta:

		abstract = True

class ApparatusThrow(Apparatus):

	pass

