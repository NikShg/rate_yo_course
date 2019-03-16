from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation

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
	rating = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)
	
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
	#should we display reviews in the userprofile?
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __str__(self):
		return self.user.username

class Rate(models.Model):
    bar = models.CharField(max_length=100)
	#ratings = GenericRelation(Rating, related_query_name='rates') #object_list


	#def __str__(self):
		#return self.name
#Rate.ratings.filter(ratings__isnull=False).order_by('ratings__average') #Foo.object_list.filter
