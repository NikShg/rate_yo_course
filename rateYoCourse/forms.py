from django import forms
from django.contrib.auth.models import User
from rateYoCourse.models import University, Course, UserProfile
from .models import Comment

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

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('user', 'body')
		
