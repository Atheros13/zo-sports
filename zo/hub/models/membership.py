from django.db import models
from datetime import datetime

class Membership(models.Model):

    ''' An abstract class that defines a time period and active status for inherited membership types.
    Has an auto_end_membership attribute which can be used to indicate when a Membership should end, 
    though it could also indicate when it needs to be renewed. '''

    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    auto_end_membership = models.DateField(null=True, blank=True)

    class Meta:

        abstract = True
