from django.contrib import admin
from rateYoCourse.models import UserProfile
from rateYoCourse.models import Course, University, Comment

# Register your models here.

class UniversityAdmin(admin.ModelAdmin):
	list_display = ('name', 'city', 'url', )
	prepopulated_fields = {'slug': ('name', 'city', 'url', )}

admin.site.register(University, UniversityAdmin)

class CourseAdmin(admin.ModelAdmin):
	list_display = ('name', 'university', 'url', )
	prepopulated_fields = {'slug': ('name', 'university', 'url',)}

admin.site.register(Course, CourseAdmin)
admin.site.register(UserProfile)

class CommentAdmin(admin.ModelAdmin):
	list_display = ('user', 'approved', 'body', 'course', 'university', )

admin.site.register(Comment, CommentAdmin)
