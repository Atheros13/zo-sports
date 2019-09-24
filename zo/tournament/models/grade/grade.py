from django.db import models
from djangoyearlessdate.models import YearlessDateField

from user.models import Gender

class AgeGrade(models.Model):



	open = models.BooleanField(default=False)
	under = models.BooleanField(default=True)
	age = models.PositiveIntegerField(null=True)
	yearless = YearlessDateField(null=True)

	def __str__(self):

		if self.open:
			return 'Open'
		elif self.under:
			return 'Under %s' % self.age
		else:
			return 'Over %s' % self.age

	def name(self, *args):

		if len(args) > 0:
			n = self.age_grade_name.filter(tournament_xxx=args[0])
			if n:
				return n[0]
		return self.__str__()	


class RankGroup(models.Model):

	''' The name of a collection of Rank objects. This provides a 
	link between the Ranks, as well as a type attribute which 
	can be used to provide more information about the group i.e. Age
	can be used as the 'type' when the RankGroup is for School Year Levels. '''

	type = models.CharField(max_length=30, blank=True)
	name = models.CharField(max_length=30)

class Rank(models.Model):

	''' A specific Rank of a RankGroup. Each Rank has to also contain 
	a rank_value which allows the Ranks in a RankGroup to be ordered 
	from lowest to highest. If this is blank, then the Ranks 
	should be ordered alphabetically '''

	rank_group = models.ForeignKey(RankGroup, on_delete=models.CASCADE,
									related_name='rank')
	name = models.CharField(max_length=30)
	rank_value = models.PositiveIntegerField(blank=True)


class Grade(models.Model):

	''' A collection of one or more age, gender and/or rank filters''' 

	age = models.ForeignKey(AgeGrade, null=True, on_delete=models.CASCADE,
								related_name='grade')
	gender = models.ForeignKey(Gender, null=True, on_delete=models.CASCADE,
								related_name='grade')
	ranks = models.ManyToManyField(Rank, related_name='grade')

	def __str__(self, *args):

		if len(args) > 0:
			n = self.name.filter(tournament=args[0])
			if n:
				return n[0].name

		name = ""
		for r in self.ranks:
			if r.rank_group.type == 'Age':
				name += '%s ' % r.name

		if self.age != None and len(args) > 0:
			name += '%s ' % self.age.name(args[0])
		elif self.age != None:
			name += '%s ' % self.age.name()		

		if self.gender != None:
			name += '%s ' % self.gender.name

		for r in self.ranks:
			if r.rank_group.type != 'Age':
				name += '%s ' % r.name

		return name.rstrip()
