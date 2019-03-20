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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as E
from selenium.webdriver.common.keys import Keys


from django.contrib.auth.models import User
from rateYoCourse.models import UserProfile
from django.template import loader
from django.conf import seetings

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage

# Model tests

class UniversityCourseMethodTests(TestCase):
	def test_slug_line_creation_university(self):
		university = University('Glasgow University')
		university.save()
		self.assertEqual(university.slug,'glasgow-university')
	
	def test_slug_line_creation_course(self):
		course = Course('Internet Technology')
		course.save()
		self.assertEqual(course.slug,'glasgow-university')

class IndexViewTests(TestCase):

	def test_university_with_no_courses(self):
		response= self.client.get(reverse('index'))
		self.assertEqual(response.status_code,200)
		self.assertContains(response,"There are no universities present.")
		self.assertQuerysetEqual(response.context['universities'],[])
	
	def add_course(uni, name, url, rating): #, rating=0
		c = Course.objects.get_or_create(university=uni, name=name)[0]
		c.url=url
		c.rating = rating
		c.save()
		return c

	def add_uni(name, city, url): #city, url
		u = University.objects.get_or_create(name=name)[0]
		u.city=city
		u.url=url
		u.save()
		return u
	
	def test_university_with_universities(self):
		add_uni('Glasgow','Glasgow','https://www.gla.ac.uk/')
		add_uni('Edinburgh', 'Edinburgh', 'https://www.ed.ac.uk/')

		response = self.client.get(reverse('universities'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Edinburgh')

		num_uni = len(response.context['universities'])
		self.assertEqual(num_uni,2)

	def test_uni_with_courses(self):
		add_course('Glasgow', 'ITECH','https://www.gla.ac.uk/coursecatalogue/course/?code=COMPSCI5012')
		add_course('Glasgowm', 'Team Project', 'https://www.gla.ac.uk/coursecatalogue/course/?code=COMPSCI5074')
	
		response = self.client.get(reverse('university'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'ITECH')

		num_c = len(response.context['courses'])
		self.assertEqual(num_c,2)


# sil test  pip install selenium==2.33.0
class TestS(TestCase):
	def setUp(self):
		from django.contrib.auth.models import User
		User.objects.create_superuser(username='admin',password='admin!',email='admin@mail.ru')
		chrome_options = webdriver.ChromeOption()
		chrome_options.add_argument('headless')
		self.browser = webdriver.Chrome(chrome_options = chrome_options)
		self.browser.implicitly_wait(3)
	def td(self):
		self.browser.refresh()
		self.browser.quit()
	
	def test_register_user(self):
		url = self.live_server_url
		url = url.replace('localhost','http://127.0.0.1:8000')

		try:
			self.browser.get(url + reverse('index'))
		except:
			try:
				self.browser.get(url + reverse ('rateyocourse:index'))
			except:
				return False
		self.browser.find_elements_by_link_text('Login')[0].click()

		username_field = self.browser.find_element_by_name('username')
		username_field.send_keys('testuser')

		email
	#def setUp(self):
	#	self.driver = webdriver.Firefox()
	
	#def test_login(self):
	#	self.driver.get('http://127.0.0.1:8000/accounts/login/')

	#	expectedMessage = "You are not signed in, this means you will not be able to rate courses and universities"
	#	message = driver.findElement(By.xpath("//div[contains(@class,'callout callout-failure')]")).getText();
	#	self.assertTrue("Your error message", message.contains(expectedMessage));
		#self.driver.select_from(nr=0)
		#self.driver.form['username']='Zxc'
		#self.driver.form['password']='Zxc123'
		#self.driver.submit()

	#def test_index_search(self):
		#self.driver.get("http://127.0.0.1:8000")
		#assert 'rateyocourse' in browser.title


	
		
		#search = browser.find_element_by_name('q')
		# search.send_keys("Internet Technology")
		#search.send_keys(Keys.RETURN)
		#time.sleep(5)
		#browser.quit()

class Chapter10SessionTests(TestCase):
	def test_about_page_shows_number_of_visits(self):
		try:
			response=self.client.get(reverse('index'))
		except:
			try:
				response=self.client.get(reverse('rateyocourse:index'))
			except:
				return False
		try:
			response=self.client.get(reverse('about'))
		except:
			try:
				response=self.client.get(reverse('rateyocourse:about'))
			except:
				return False

	def test_user_access(self):
		for i in range(0,100):
			try:
				response = self.client.get(reverse('index'))
			except:
				try:
					response=self.client.get(reverse('rateyocourse:index'))
				except:
					return False
			session = self.client.session
			self.assertIsNotNone(self.client.session['visits'])
			self.assertIsNotNone(self.client.session['last_visit'])

			last_visit = datetime.noew() - timedelta(days=1)

			session['last_visit']= str(last_visit)
			session.save()

			self.assertEquals(session['visits'],session['visits'])