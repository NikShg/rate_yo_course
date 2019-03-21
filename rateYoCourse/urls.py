from django.conf.urls import url
from rateYoCourse import views
#from django.contrib.auth import views as auth_views
from django.conf.urls import include

urlpatterns = [
	url(r'^$', views.index, name='index'), 
	url(r'^about/$', views.about, name='about'),
	url(r'^universities/(?P<university_name_slug>[\w\-]+)/$', views.show_university, name='university'), # for showing a specific uni
	url(r'^universities/$', views.show_university_, name='universities'), # showing all unis
	# showing a specific course
	url(r'^universities/(?P<university_name_slug>[\w\-]+)/courses/(?P<course_name_slug>[\w\-]+)/$', views.show_course, name='course'), 
	# registration a profile (step 2)
	url(r'^register_profile/$', views.register_profile, name='register_profile'),
	# viewing a user's profile
	url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
	# viewing all profiles
	url(r'^profiles/$', views.list_profiles, name='list_profiles'),
	# search page
    url(r'^search/$', views.search, name = 'search'),
	# when searching for either university or course
	url(r'^search/(?P<university_name_slug>[\w\-]+)/$', views.show_university, name='course'),
	url(r'^search/(?P<course_name_slug>[\w\-]+)/$', views.show_course, name='course'),
	# for logging via twitter or github apps
	url(r'^accounts/', include('allauth.urls')),
	url(r'^social-auth/', include('social_django.urls', namespace="social")),
	]
