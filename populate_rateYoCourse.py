import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rate_yo_course.settings')


import django
django.setup()
from rateYoCourse.models import University, Course

def populate():
    UoG_courses = [
        {"name": "Internet Technology", "url": "https://www.gla.ac.uk/postgraduate/taught/informationtechnology/?card=course&code=COMPSCI5012"},
        {"name": "Advanced Programming", "url": "https://www.gla.ac.uk/postgraduate/taught/softwaredevelopment/?card=course&code=COMPSCI5002"}
    ]

    University_of_Edinburgh_courses = [
        {"name":"Computer Science BSc", "url":"https://www.ed.ac.uk/studying/undergraduate/degrees/index.php?action=programme&code=G400"},
        {"name":"Artificial Intelligence BSc", "url":"https://www.ed.ac.uk/studying/undergraduate/degrees/index.php?action=programme&code=G700"},
    ]

    unis = {"UoG": {"courses": UoG_courses},
            "University of Edinburgh": {"courses": University_of_Edinburgh_courses}}

    for uni, uni_data in unis.items():
        u = add_uni(unis) #city, url
        for c in uni_data["courses"]:
            add_course(u, c["name"], c["url"])

    for u in University.objects.all():
        for c in Course.objects.filter(university=u):
            print("- {0} - {1}".format(str(u), str(c)))

def add_course(uni, name, url):
    c = Course.objects.get_or_create(university=uni, name=name)[0]
    c.url=url
    c.save()
    return c

def add_uni(name): #city, url
    u = University.objects.get_or_create(name=name)[0]
    #u.city=city
    #u.url=url
    u.save()
    return u

if __name__ == '__main__' :
    print("Starting RateYoCourse population script...")
    populate()
