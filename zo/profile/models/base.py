from django.db import models
from django.contrib.postgres.fields import ArrayField

class Gender(models.Model):

    gender = models.CharField(max_length=30, unique=True)

class FullName(models.Model):

    '''
    '''

    firstname = models.CharField(max_length=50)
    middlenames = ArrayField(models.CharField(max_length=50))
    surname = models.CharField(max_length=30)
    
    preferred_firstname = models.CharField(max_length=50, blank=True, 
                                           default='')

    def __str__(self):

        firstname = self.firstname
        if self.preferred_firstname:
            firstname = self.preferred_firstname
        
        return '%s %s' % (firstname, self.surname)

    def fullname(self, preferred=True):

        firstname = self.firstname
        if preferred == True and self.preferred_firstname != '':
            firstname = self.preferred_firstname

        return '%s %s %s' % (firstname, self.middlenames.join(' '), self.surname)

class GPS(models.Model):

	longitude = models.DecimalField(max_digits=9, decimal_places=6)
	latitude = models.DecimalField(max_digits=9, decimal_places=6)

class Address(models.Model):

	gps = models.ForeignKey(GPS, null=True, on_delete=models.CASCADE)
	
	line1 = models.CharField(max_length=50)
	line2 = models.CharField(max_length=50)
	line3 = models.CharField(max_length=50)
	town_city = models.CharField(max_length=50)
	postcode = models.CharField(max_length=50)
	country = models.CharField(max_length=50)

class ContactDetails(models.Model):

	phone_landline = models.CharField(max_length=30, blank=True) # numeric validators
	phone_mobile = models.CharField(max_length=30, blank=True) # numeric validators
	address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
	email = models.EmailField()

