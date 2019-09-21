from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from tournament.models.activity import Activity

class Contest(models.Model):

	''' Returns a ContestType object or multiple ContestType objects. '''

	CHOICES_CONTEST_TYPE = {'pk__in':ContentType.objects.all().filter(model__startswith='contest type')} 

	activity = models.ForeignKey(Activity, null=True, on_delete=models.SET_NULL, related_name='contests')
	contests = models.ManyToManyField('self')

	content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE, limit_choices_to=CHOICES_CONTEST_TYPE)
	object_id = models.PositiveIntegerField()
	contest = GenericForeignKey('content_type', 'object_id')

	def __str__(self, *args):

		if len(args) > 0:
			n = self.name.filter(tournament=args[0])
			if n:
				return n[0].name
		if len(self.contests) > 0:
			return '%s Contests' % len(self.contests)
		return self.contest.__str__()

class ContestType(models.Model):

	''' An abstract base class for all types/forms of Contests. It includes
    a reverse relationship to the actual Contest object. '''

	contest = GenericRelation(Contest)

	class Meta:

		abstract = True

	def __str__(self):
		
		return self.__class__.__name__
