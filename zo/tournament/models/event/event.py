from django.db import models

from tournament.models.contest import Contest
from tournament.models.grade import Grade

class Event(models.Model):

    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='events')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='events')

    def __str__(self, *args):
        if len(args) > 0:
            return '%s %s' % (self.grade.__str__(args[0]), self.contest.__str__(args[0]))
        return '%s %s' % (self.grade.__str__(), self.contest.__str__())
