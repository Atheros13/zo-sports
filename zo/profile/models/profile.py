from django.db import models

from profile.models.base import *

class Profile(models.Model):

    #user = 
    person = models.ForeignKey('Person', null=True, 
                               on_delete=models.CASCADE)
    contact_details = models.ForeignKey(ContactDetails, null=True, 
                                        on_delete=models.CASCADE)

class PersonGender(models.Model):

    gender = models.ForeignKey(Gender, related_name='gender_identity',
                               on_delete=models.CASCADE)
    birth_gender = models.ForeignKey(Gender, related_name='birth_gender',
                                     on_delete=models.CASCADE, null=True)

class PersonName(models.Model):

    '''
    '''

    name = models.ForeignKey(FullName, related_name='current_name',
                             on_delete=models.CASCADE)
    birth_name = models.ForeignKey(FullName, related_name='birth_name',
                                   on_delete=models.CASCADE)

class Person(models.Model):

    '''
    '''

    name = models.ForeignKey(PersonName, on_delete=models.CASCADE)
    gender = models.ForeignKey(PersonGender, null=True, on_delete=models.CASCADE)
    dob = models.DateField(verbose_name='Date of Birth', null=True)

