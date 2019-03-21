#This is a population script to populate RateYoCourse database with sample data. The data in this document is incomplete and is used fo demo purposes.
#

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rate_yo_course.settings')

import django
django.setup()
from rateYoCourse.models import University, Course


def populate():
    #Here is a list of dictionaries containing the courses we want to add to each university
    #This section also includes a dictionary of the dictionaries to allow us to iterate through each datastructure,
        #and add the data to the models.
    University_of_Glasgow_courses = [
        {"name": "Internet Technology", "url": "https://www.gla.ac.uk/postgraduate/taught/informationtechnology/?card=course&code=COMPSCI5012", "rating": 5},
        {"name": "Advanced Programming", "url": "https://www.gla.ac.uk/postgraduate/taught/softwaredevelopment/?card=course&code=COMPSCI5002", "rating": 3}
    ]

    University_of_Edinburgh_courses = [
        {"name":"Computer Science BSc", "url": "https://www.ed.ac.uk/studying/undergraduate/degrees/index.php?action=programme&code=G400", "rating": 0},
        {"name":"Artificial Intelligence BSc", "url": "https://www.ed.ac.uk/studying/undergraduate/degrees/index.php?action=programme&code=G700", "rating": 1},
    ]

    unis = {"University of Glasgow": {"courses": University_of_Glasgow_courses, "city": "Glasgow", "url": "https://www.gla.ac.uk"}, "University of Edinburgh": {"courses": University_of_Edinburgh_courses, "city": "Edinburgh", "url": "https://www.ed.ac.uk"}}

    #This code goes through the uni dictionary, then adds each university,
        #then adds the associated courses for that university.
    for uni, uni_data in unis.items():
        u = add_uni(uni, uni_data["city"], uni_data["url"]) #city, url
        for c in uni_data["courses"]:
            add_course(u, c["name"], c["url"], c["rating"])

    #print out the universities we have added.
    for u in University.objects.all():
        for c in Course.objects.filter(university=u):
            print("- {0} - {1}".format(str(u), str(c)))

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

#execution starts here
if __name__ == '__main__' :
	print("Starting rateYoCourse population script...")
	populate()
