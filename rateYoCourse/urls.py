from django.conf.urls import url 
from rateYoCourse import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^about/', views.about, name='about'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^register_profile/$', views.register_profile, name='register_profile'),
	url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
	url(r'^profiles/$', views.list_profiles, name='list_profiles'),
	]
