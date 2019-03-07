from django.contrib import admin
from rateYoCourse.models import UserProfile
from rateYoCourse.models import Course, University

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(University)
