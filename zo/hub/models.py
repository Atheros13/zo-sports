from django.db import models

from user.models import ContactDetails, CustomUser

# Create your models here.

class Hub(models.Model):

	CHOICES_HUB_TYPE = [
		('School', 'School'), ('Sports Club', 'Sports Club'),
		('Other', 'Other'),
	    ]

	# 
	type = models.CharField(max_length=30, choices=CHOICES_HUB_TYPE)
	name = models.CharField(max_length=30)
	contact_details = models.ForeignKey(ContactDetails, on_delete=models.CASCADE, null=True)
	main_contact = models.ForeignKey(CustomUser, related_name='main_contact',
                                  on_delete=models.CASCADE, null=True)

	# Permissions
	permission_admin = models.ManyToManyField(CustomUser, related_name='permission_admin')
	permission_staff = models.ManyToManyField(CustomUser, related_name='permission_staff')
	is_public = models.BooleanField(default=False)

	class Meta:

		pass

	def __str__(self):
		return self.name

	def has_admin(self, user):

		if user in permission_admin or user == main_contact:	
			return True
		return False

	def has_staff(self, user):

		if user in permission_staff or user == main_contact or user in permission_admin:
			return True
		return False