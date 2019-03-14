from django import forms
from django.contrib.auth.models import User
from rateYoCourse.models import University, Course, UserProfile

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		
class UserProfileForm(forms.ModelForm):
	picture = forms.ImageField(required=False)
	
	class Meta:
		model = UserProfile
		exclude = ('user', )