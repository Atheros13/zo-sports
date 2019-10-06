from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from datetime import datetime

class MembershipType(models.Model):

    ''' An abstract model which can be inherited to create a unique 
    membership type for ... '''

    type = None
    name = models.CharField(max_length=30)
    super_type = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_types')

    class Meta:

        abstract = True

    def __str__(self):

        pass

class MembershipPeriod(models.Model):
    
    ''' '''

    CHOICES = {'pk__in':ContentType.objects.all().filter(model__endswith='membership')} 

    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE, limit_choices_to=CHOICES)
    object_id = models.PositiveIntegerField()

    membership = GenericForeignKey('content_type', 'object_id')
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def __str__(self):

        name = '%s: ' % self.membership.__str__()
        if self.start_date:
            name += '%s' % self.start_date
        else:
            return name + 'start and end dates not provided'
        if self.end_date:
            return name + ' - %s' % self.end_date
        return name + ' - currently'

class Membership(models.Model):

    ''' '''

    MEMBER_RELATED_NAME = ''

    membership = None
    member = models.ForeignKey(HubMember, on_delete=models.CASCADE, related_name=MEMBER_RELATED_NAME)
    membership_periods = GenericRelation(MembershipPeriod)

    class Meta:

        abstract = True

    def add(self, start_date=None, end_date=None):

        ''' Creates a membership_period and links it to this Membership. If a current period 
        is still active it will renew that one instead. '''

        mp = self.membership_periods.order_by(-start_date)
        if mp:
            if mp[0].end_date == None or mp[0].end_date < datetime.now():
                self.renew(end_date=end_date)
                return
        
        if start_date == None:
            start_date = datetime.now()

        MembershipPeriod(content_type=ContentType.objects.get_for_model(self),
                             id=self.id, start_date=start_date, end_date=end_date).save()

    def is_active(self):

        ''' Returns True if the current membership_period end_date == None, 
        or if it is greater than the current date, and False if it is less than the current date, 
        or it there are no membership_periods connected to this Membership. '''

        mp = self.membership_periods.order_by(-start_date)
        if mp:
            if mp[0].end_date:
                return mp[0].end_date >= datetime.now()
            return True
        return False

    def renew(self, end_date=None):

        ''' Renews the most recent membership_period, by either changing the 
        end_date to a set date or to None. '''

        mp = self.membership_periods.order_by(-start_date)
        if mp:
            if end_date == None or end_date > datetime.now():
                mp[0].end_date = end_date
                mp[0].save()

    def cancel(self, end_date=None):

        ''' Cancels the most recent membership_period, by either changing the 
        end_date to the current date or an earlier date. '''

        mp = self.membership_periods.order_by(-start_date)
        if mp:
            if end_date == None or end_date > datetime.now():
                mp[0].end_date = datetime.now()
            else:
                mp[0].end_date = end_date
            mp[0].save()

