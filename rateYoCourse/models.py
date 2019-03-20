from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from star_ratings.models import Rating, UserRating
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import Truncator

# Create your models here.

class University(models.Model):
	name = models.CharField(max_length=128, unique=True, null=False)
	city = models.CharField(max_length=32, null=False)
	url = models.URLField(null=False)
	slug = models.SlugField(unique=True)

	@property
	def get_photo_url(self):
		return 'images/%s.jpg' % self.name

	def save(self, *args, **kwargs):
		self.name=self.name[:128]
		self.city=self.city[:32]
		self.slug = slugify(self.name)
		super(University, self).save(*args, **kwargs)

	class Meta:
		verbose_name_plural = 'universities'

	def __str__(self):
		return self.name

class Course(models.Model):
	university = models.ForeignKey(University)
	name = models.CharField(max_length=256, null=False)
	url = models.URLField(null=False)
	slug = models.SlugField(unique=True)

	@property
	def get_university_slug(self):
		return self.university.slug

	@property
	def get_photo_url(self):
		return 'images/%s.jpg' % self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Course, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	about = models.CharField(max_length=256)
	status = models.CharField(max_length=256)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __str__(self):
		return self.user.username

class Rate(models.Model):
    bar = models.CharField(max_length=100)
	

class Comment(models.Model): #post = Course
	university = models.ForeignKey(University, related_name="university")
	course = models.ForeignKey(Course, related_name='course') #Course?
	user = models.ForeignKey(UserProfile, related_name='user_name') #if it doesn't work try 'user = models.OneToOneField(User)'
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def approved(self):
		self.approved = True
		self.save()
