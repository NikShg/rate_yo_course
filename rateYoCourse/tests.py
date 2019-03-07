from django.test import TestCase
#from rango.models import UniverityCourse
# Create your tests here.

class UniversityCourseMethodTests(TestCase):
	def test_ensure_views_are_positive(self):
	
		cat = UniversityCourse(name='test', review=-1, likes=0)
		cat.save()
		self.assertEqual((cat.reviews >=0), True)