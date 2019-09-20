from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from tournament.models.tournament import Tournament

class Contest(models.Model):

	''' Returns a ContestType object or multiple ContestType objects. '''

	CHOICES_CONTEST_TYPE = {'pk__in':ContentType.objects.all().filter(model__startswith='contest type')} 

	contests = models.ManyToManyField('self')

	content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE, limit_choices_to=CHOICES_CONTEST_TYPE)
	object_id = models.PositiveIntegerField()
	contest = GenericForeignKey('content_type', 'object_id')



	def __str__(self, *args):

		if len(args) > 0:
			name = self.name.filter(tournament=args[0])
			if name:
				return name.name
		if len(self.contests) > 0:
			return '%s Contests' % len(self.contests)
		return self.contest.__str__()

class ContestName(models.Model):

	''' A name used by a Tournament to refer to a Contest i.e. "100m Dash" or "100m Sprint". 
    This can be used when the Contest is actually made up of multiple Contests i.e. 
    a Decathlon, or when the __str__() method doesn't return the name that a Tournament uses.'''
	
	name = models.CharField(max_length=30)
	contest = models.ForeignKey(Contest, on_delete=models.CASCADE,
								related_name='name')
	tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE,
								related_name='contest_name') 

	def __str__(self):
		return self.name

class ContestType(models.Model):

	''' An abstract base class for all types/forms of Contests. It includes
    a reverse relationship to the actual Contest object, and (currently) a
    file link where a document containing the rules, regulations and instructions
    can be stored and retrieved. '''

	contest = GenericRelation(Contest)

	class Meta:

		abstract = True

	def __str__(self):
		
		return self.__class__.__name__
