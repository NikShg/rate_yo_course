"""rate_yo_course URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from rateYoCourse import views
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.views import (password_reset, password_reset_done, password_reset_confirm, password_reset_complete, password_change, password_change_done)
from django.core.urlresolvers import reverse

class MyRegistrationView(RegistrationView):
	def get_success_url(self, user):
		return reverse('register_profile')

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^rateyocourse/', include('rateYoCourse.urls')),
    url(r'^admin/', admin.site.urls),
	url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
	url(r'^accounts/profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
	url(r'^accounts/profile/$', views.list_profiles, name='list_profiles'),
	url(r'^accounts/password/change/$', password_change, name='password_change_form'),
	url(r'^accounts/password/change/done/$', password_change_done, name='password_change_done'),
	url(r'^accounts/password/reset/$', password_reset, name='password_reset'),
	url(r'^accounts/password/reset/done/$', password_reset_done, name='password_reset_done'),
	url(r'^university/(?P<university_name_slug>[\w\-]+)/$', views.show_university, name='university'),
	url(r'^university/$', views.show_university_, name='universities'),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),##NEEDED?
    url(r'^university/(?P<university_name_slug>[\w\-]+)/courses/(?P<course_name_slug>[\w\-]+)/$', views.show_course, name='course'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
