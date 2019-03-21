from django import forms
from django.contrib.auth.models import User
from rateYoCourse.models import University, Course, UserProfile
from rateYoCourse.models import Comment

# selections for a student to choose in step 2 of registering their account/profile
STUDENT_CHOICES = [
	('Prospective Student', 'Prospective Student'),
	('Current Student', 'Current Student'),
	('Alumni', 'Alumni'),
]

# masks the password when user enters password in registration or login forms
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

# 2nd registration step for profile , pictures, status, about - all aren't required allowing user to come back to finish
class UserProfileForm(forms.ModelForm):
	picture = forms.ImageField(required=False)
	status = forms.CharField(label='What is your current status?', widget=forms.Select(choices=STUDENT_CHOICES), required=False)
	about = forms.CharField(required=False, widget=forms.Textarea)


	class Meta:
		model = UserProfile
		exclude = ('user', )

# form when a user wants to add a comment
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('body', )
