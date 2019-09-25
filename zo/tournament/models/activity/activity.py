from django.db import models

class ActivityType(models.Model):

    ''' The category that an Activity belongs to i.e. Sport. '''

    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, default='')

class Activity(models.Model):

    ''' The specific Activity in a ActivityType i.e. Athletics, 
    this can also contain other sub_activities (reverse related) 
    i.e. Track and Field Activities are sub_activities of Athletics. '''

    type = models.ForeignKey(ActivityType, null=True, 
                             on_delete=models.CASCADE,
                             related_name='activities')
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, default='')

    super_activity = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='sub_activities')
