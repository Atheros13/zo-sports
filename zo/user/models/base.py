from django.db import models
from django.contrib.postgres.fields import ArrayField

class Gender(models.Model):

    gender = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.gender

class FullName(models.Model):

    '''
    '''

    firstname = models.CharField(verbose_name='First Name', max_length=50)
    middlenames = models.CharField(verbose_name='Middle Name/s', max_length=50, 
                                   blank=True)
    surname = models.CharField(max_length=30)
    
    preferred_name = models.CharField(verbose_name='Preferred Name', max_length=50, 
                                      blank=True, default='')

    def __str__(self):

        firstname = self.firstname
        if self.preferred_name:
            firstname = self.preferred_name
        
        return '%s %s' % (firstname, self.surname)

    def fullname(self, preferred=True):

        firstname = self.firstname
        if preferred == True and self.preferred_firstname != '':
            firstname = self.preferred_firstname

        return '%s %s %s' % (firstname, self.middlenames, self.surname)

class GPS(models.Model):

	longitude = models.DecimalField(max_digits=9, decimal_places=6)
	latitude = models.DecimalField(max_digits=9, decimal_places=6)

class Address(models.Model):

	gps = models.ForeignKey(GPS, null=True, on_delete=models.CASCADE)
	
	line1 = models.CharField(verbose_name='Address Line 1', max_length=50)
	line2 = models.CharField(verbose_name='Address Line 2',max_length=50, blank=True)
	line3 = models.CharField(verbose_name='Address Line 3',max_length=50, blank=True)
	town_city = models.CharField(verbose_name='Town/City',max_length=50)
	postcode = models.CharField(verbose_name='Postcode',max_length=50, blank=True)
	country = models.CharField(verbose_name='Country',max_length=50, blank=True)

class ContactDetails(models.Model):

	phone_landline = models.CharField(max_length=30, blank=True) # numeric validators
	phone_mobile = models.CharField(max_length=30, blank=True) # numeric validators
	address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
	email = models.EmailField()

