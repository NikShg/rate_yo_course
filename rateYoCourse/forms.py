from django import forms
from django.contrib.auth.models import User
from rateYoCourse.models import University, Course, UserProfile

STUDENT_CHOICES = [
	('Prospective Student', 'Prospective Student'),
	('Current Student', 'Current Student'),
	('Alumni', 'Alumni'),
]

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		
class UserProfileForm(forms.ModelForm):
	picture = forms.ImageField(required=False)
	status = forms.CharField(label='What is your current status?', widget=forms.Select(choices=STUDENT_CHOICES), required=False)
	about = forms.CharField(required=False, widget=forms.Textarea)
	
	
	class Meta:
		model = UserProfile
		exclude = ('user', )

	