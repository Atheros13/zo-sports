from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from tournament.models.tournament import Tournament
from tournament.models.contest import Contest

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