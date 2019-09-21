from django.db import models

class ActivityType(models.Model):

    name = models.CharField(max_length=30)
    description = models.TextField()

class Activity(models.Model):

    type = models.ForeignKey(ActivityType, null=True, 
                             on_delete=models.CASCADE,
                             related_name='activities')
    name = models.CharField(max_length=30)
    description = models.TextField()

    sub_activities = models.ManyToManyField('self')
