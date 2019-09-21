from django.db import models
from djangoyearlessdate.models import YearlessDateField

from tournament.models.grade import AgeGrade, Grade
from tournament.models.tournament import Tournament

class AgeGradeName(models.Model):

	''' An AgeGrade is a set of filters, and does not have an actual
	name attribute. Usually the name will be Under 14 or Open etc, however
	as some tournaments will name this grade something unique i.e. Junior, 
	Senior, U14 etc, this links a name to an AgeGrade and a Tournament. '''

	name = models.CharField(max_length=30)
	age_grade = models.ForeignKey(AgeGrade, on_delete=models.CASCADE, 
									related_name='age_grade_name')
	tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE,
                                    related_name='age_grade_name')

	def __str__(self):
	    return self.name

class GradeName(models.Model):

	''' A Grade is a collection of filters, and does not have an actual 
	name attribute. A __str__() can be derived from the filters, but 
	sometimes a Tournament will have a unique Grade name they want to use '''

	name = models.CharField(max_length=50)
	grade = models.ForeignKey(Grade, on_delete=models.CASCADE,
								related_name='name')
	tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE,
									related_name='grade_names')