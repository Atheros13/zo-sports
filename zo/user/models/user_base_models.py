from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail, BadHeaderError
from django.contrib.postgres.fields import ArrayField

### BASE MODELS ###

class Gender(models.Model):

    gender = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.gender

class NameBase(models.Model):

    ''' An abstract name class which can be inherited by other models. '''

    firstname = models.CharField(verbose_name='First Name', max_length=50)
    middlenames = models.CharField(verbose_name='Middle Name/s', max_length=50, 
                                   blank=True)
    surname = models.CharField(max_length=30)
    
    preferred_name = models.CharField(verbose_name='Preferred Name', max_length=50, 
                                      blank=True, default='')

    class Meta:
        abstract = True

    def __str__(self):
        firstname = self.firstname
        if self.preferred_name:
            firstname = self.preferred_name
        
        return '%s %s' % (firstname, self.surname)

    def name(self):
        if self.preferred_name:
            return self.preferred_name
        return self.firstname

    def fullname(self, preferred=True):

        firstname = self.firstname
        if preferred == True and self.preferred_firstname != '':
            firstname = self.preferred_firstname

        return '%s %s %s' % (firstname, self.middlenames, self.surname)

class Name(NameBase):

    ''' A NameBase inherited model, for use with a CustomUser. '''

    user_name = models.OneToOneField('CustomUser', null=True, 
                                    on_delete=models.CASCADE, related_name='name')
    user_birth = models.OneToOneField('CustomUser', null=True, 
                                    on_delete=models.CASCADE, related_name='birth_name')
 

### USER MODELS ###

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

    ## OWN ATTRIBUTES
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_huttscience = models.BooleanField(default=False)

    ## OUT ATTRIBUTES
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, related_name='custom_user')
    birth_gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, related_name='custom_user_birth')

    ### MISC ###
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    ### IN ATTRIBUTES ###
    # name
    # birth_name
    
    ### META DATA ###
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

        
    def __str__(self):
        try:
            return self.name.__str__()
        except:
            return self.email

    ### FUNCTIONS ###
    def email_user(self, subject, message, from_email='no-reply@zo-sports.com', **kwargs):
        ''' Sends an email to this User. '''

        send_mail(subject, message, from_email, [self.email])

### USER ADJACENT MODELS ###

class TemporaryPassword(models.Model):

    password = models.CharField(max_length=30)
    is_temp = models.BooleanField(default=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Signup(models.Model):

    firstname = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    message = models.TextField(blank=True)
    is_staff = models.BooleanField(default=False)

    def create_custom_user(self):

        password = CustomUser.objects.make_random_password()

        user = CustomUser(email=self.email, is_staff=self.is_staff,
                          phone_number=self.phone)
        user.set_password(password)
        user.save()

        name = Name(firstname=self.firstname, surname=self.surname)
        name.user = user
        name.save()

        # Creates a reference to this 
        temp = TemporaryPassword(password=password, user=user)
        temp.save()

        user.email_user('ZO-SPORTS Login', self.create_login_email(password))

    def create_login_email(self, password):

        message = 'Hi %s,\n\n' % self.firstname
        message += 'You can now log in at www.zo-sports.com/login '
        message += 'using the following details:\n\n'
        message += 'Username: %s\nTemporary Password: %s\n\n' % (self.email, password)
        message += 'When you first log in, you will be asked to set a new password '
        message += 'and complete some of your profile.\n\n'
        message += 'If you ever need to contact us, please use the Contact form on the '
        message += 'main website.\n\nWelcome to ZO-SPORTS.'

        return message

class PasswordReset(models.Model):

    reference = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def send_reset_link(self):

        message = 'Hi %s,\n\n' % self.user.name
        message += 'You have requested to reset the password to your ZO-SPORTS login. '
        message += 'The link to reset your password is below:\n\n'
        message += 'www.zo-sports.com/password_reset/%s \n\n' % self.reference
        message += 'If you did not request this reset, please ignore this email or if '
        message += 'you are concerned about security, contact ZO-SPORTS through the website.'
        message += '\n\nKind regards,\n\nZO-SPORTS'

        self.user.email_user('ZO-SPORTS Password Reset', message)
