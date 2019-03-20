from django.test import TestCase
from rateYoCourse.models import University, Course, Rate
from star_ratings.models import Rating, UserRating
#from rango.models import UniverityCourse
# Create your tests here.

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
		
		
