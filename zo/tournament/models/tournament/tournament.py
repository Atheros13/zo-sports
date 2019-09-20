from django.db import models

class TournamentMaster(models.Model):

	''' The base blueprint for a series of Tournaments, i.e. The McEvedy Shield,
	which will have an inherited/linked Tournament object for each year. 
	Tournament objects inherit much of the data from TournamentMaster, but vary 
	in Participants and perhaps minor TournamentEvent differences, etc. 
	The TournamentMaster can change over time, previous Tournaments that 
	derive from the old versions will act as a record.'''

	name = models.CharField(max_length=30)


	#events = models.ManyToManyField(Event)

class Tournament(models.Model):

	''' 
	'''

	master = models.ForeignKey(TournamentMaster, null=True, 
								on_delete=models.SET_NULL, 
								related_name='tournament')

	name = models.CharField(max_length=50)


	#events = models.ManyToManyField(TournamentEvent, related_name='tournament')
