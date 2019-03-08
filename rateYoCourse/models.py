from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class University(models.Model):
	name = models.CharField(max_length=128, unique=True, null=False)
	city = models.CharField(max_length=32, null=False)
	url = models.URLField(null=False)

	class Meta:
		verbose_name_plural = 'Universities'

	def __str__(self):
		return self.name

class Course(models.Model):
	name = models.CharField(max_length=256, null=False)
	url = models.URLField(null=False)
	university = models.ForeignKey(University)
	#university = models.ForeignKey(University, null=False)

	def __str__(self):
		return self.name

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	#should we display reviews in the userprofile?
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __str__(self):
		return self.user.username
