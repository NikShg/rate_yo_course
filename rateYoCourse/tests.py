from django.test import TestCase
from rateYoCourse.models import University, Course, Rate
from star_ratings.models import Rating, UserRating
from django.contrib.staticfiles import finders
import populate_rateYoCourse
from django.core.urlresolvers import reverse

class UniversityCourseMethodTests(TestCase):
	def test_city_is_not_more_than_32_chars(self):
		'''
		Test that university city is limited to 32 characters
		'''
		university = University(name="University of London", city="abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", url="www.uol.com")
		university.save()
		self.assertEqual((len(university.city) <= 32), True)
		
	def  test_university_name_is_not_more_than_128_chars(self):
		'''
		Test that university name is limited to 128 characters
		'''
		university = University(name="The Brilliant, Most Expensive University For the Most Beautiful People On Planet Earth Known To Mankind In The Year 2019 That Only Teaches ITech", city="Neverland", url="www.uniwithlongname.com")
		university.save()
		self.assertEqual((len(university.name) <= 128), True)	
		
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


	def test_correct_image_url(self):
		'''
		Test that url path to images is as expected
		'''
		university = University.objects.create(name="University of Glasgow", city="Glasgow", url="www.gla.ac.uk")
		course = Course(university=university, name="Internet Technology", url="https://www.gla.ac.uk/postgraduate/taught/informationtechnology/")
		course.save()
		itech = course.get_photo_url
		self.assertEqual(itech, 'images/Internet Technology.jpg')
		
class RateMethodTest(TestCase):
	def test_bar_length(self):
		#Test max length validator
		rate = Rate(bar=120)
		rate.save()
		self.assertEqual((rate.bar <=100), True)
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