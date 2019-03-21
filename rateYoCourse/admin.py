from django.contrib import admin
from rateYoCourse.models import UserProfile
from rateYoCourse.models import Course, University, Comment

#University section - displaying columns for university names, their locations and their websites
class UniversityAdmin(admin.ModelAdmin):
	list_display = ('name', 'city', 'url', )
	prepopulated_fields = {'slug': ('name', 'city', 'url', )}

admin.site.register(University, UniversityAdmin)

#Courses section - displaying columns for course names, the universities that provide them and their websites
class CourseAdmin(admin.ModelAdmin):
	list_display = ('name', 'university', 'url', )
	prepopulated_fields = {'slug': ('name', 'university', 'url',)}

admin.site.register(Course, CourseAdmin)
admin.site.register(UserProfile)

#Comments display users, approved, contents, course and universities their linked with
class CommentAdmin(admin.ModelAdmin):
	list_display = ('user', 'approved', 'body', 'course', 'university', )

admin.site.register(Comment, CommentAdmin)
