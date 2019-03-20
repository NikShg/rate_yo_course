from django.test import TestCase
#from rango.models import UniverityCourse
# Create your tests here.
from rateYoCourse.models import University, Course
from django.core.urlresolvers import reverse
import os
import os.path
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
import populate_rateYoCourse
from datetime import datetime, timedelta
import socket

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as E
from selenium.webdriver.common.keys import Keys


from django.contrib.auth.models import User
from rateYoCourse.models import UserProfile
from django.template import loader
from django.conf import settings

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage

from django.contrib.staticfiles import finders

# Model tests

class testView(TestCase):
	def test_index(self):
		response = self.client.get(reverse('index'))
		self.assertIn('Welcome to Rate Yo Course'.lower(), response.content.decode('ascii').lower())
	
	def test_about_contains_create_message(self):
		self.client.get(reverse('index'))
		response = self.client.get(reverse('about'))
		self.assertIn('About our team'.lower(),response.content.decode('ascii').lower())

class testView2(TestCase):
	def test_about_using_template(self):
		self.client.get(reverse('index'))
		response = self.client.get(reverse('about'))

		self.assertTemplateUsed(response,'rateyocourse/about.html')
	
	def test_static_files(self):
		result = finders.find('images/team.jpg')
		self.assertIsNotNone(result)

class test_models(TestCase):
	def test_create_a_new_uni(self):
		uni = University(name="Glasgow")
		uni.save()

		uni_in_data = University.objects.all()
		self.assertEquals(len(uni_in_data),1)
		only = uni_in_data[0]
		self.assertEquals(only, uni)

	def test_create_a_course_for_unis(self):
		uni = University(name="Glasgow")
		uni.save()

		course_data = Course()
		course_data.uni= uni
		course_data.uni.name="ITECH"
		course_data.uni.url="https://www.gla.ac.uk/postgraduate/taught/informationtechnology/?card=course&code=COMPSCI5012"
		course_data.save()

		course_data = uni.course.set_all()
		first_page = course_data[0]

		self.assertEquals(first_page)