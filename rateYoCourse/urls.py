from django.conf.urls import url
from rateYoCourse import views
#from django.contrib.auth import views as auth_views
from django.conf.urls import include

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^about/$', views.about, name='about'),
	url(r'^universities/(?P<university_name_slug>[\w\-]+)/$', views.show_university, name='university'),
	url(r'^universities/$', views.show_university_, name='universities'),
	url(r'^universities/(?P<university_name_slug>[\w\-]+)/courses/(?P<course_name_slug>[\w\-]+)/$', views.show_course, name='course'),
	url(r'^goto/$', views.track_url, name='goto'),
	url(r'^register_profile/$', views.register_profile, name='register_profile'),
	url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
	url(r'^profiles/$', views.list_profiles, name='list_profiles'),
    url(r'^search/$', views.search, name = 'search'),
	url(r'^search/(?P<university_name_slug>[\w\-]+)/$', views.show_university, name='course'),
	url(r'^search/(?P<course_name_slug>[\w\-]+)/$', views.show_course, name='course'),
	url(r'^oauth/', include('social_django.urls', namespace='social')),
	url(r'^accounts/', include('allauth.urls')),
	url(r'^social-auth/', include('social_django.urls', namespace="social")),
	]