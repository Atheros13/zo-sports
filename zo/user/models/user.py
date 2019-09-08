from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser

from user.models.base import *

class PersonGender(models.Model):

    gender = models.ForeignKey(Gender, related_name='gender_identity',
                               on_delete=models.CASCADE)
    birth_gender = models.ForeignKey(Gender, related_name='birth_gender',
                                     on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.gender.__str__()

class PersonName(models.Model):

    '''
    '''

    name = models.ForeignKey(FullName, related_name='current_name',
                             on_delete=models.CASCADE)
    birth_name = models.ForeignKey(FullName, related_name='birth_name',
                                   on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name.__str__()

class Person(models.Model):

    '''
    '''

    name = models.ForeignKey(PersonName, on_delete=models.CASCADE)
    gender = models.ForeignKey(PersonGender, null=True, on_delete=models.CASCADE)
    dob = models.DateField(verbose_name='Date of Birth', null=True)

    #memberships
    #participations

    def __str__(self):
        return self.name.__str__()


class CustomUserManager(BaseUserManager):
    
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_huttscience = models.BooleanField(default=False)
    
    person = models.OneToOneField(Person, on_delete=models.CASCADE, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):

        if self.person != None:
            return self.person.name.__str__()
        return self.email

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        pass

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        pass

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message,
                      from_email, ['info@zo-sports.com'])

    def signup(self, signup):   

        self.email = signup.email
        self.phone_number = signup.phone
        self.is_staff = signup.is_staff

        name = FullName(firstname=signup.firstname, surname=signup.surname)
        name.save()
        person_name = PersonName(name=name)
        person_name.save()
        person = Person(name=person_name)
        person.save()
        self.person = person
        self.save()

        message = 'Hi %s, welcome to ZO-SPORTS,\n\n' % signup.firstname
        message += ''

        self.email_user('ZO-SPORTS Login', message, 'no-reply@zo-sports.com')



class Signup(models.Model):

    firstname = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    message = models.TextField(blank=True)
    is_staff = models.BooleanField(default=False)