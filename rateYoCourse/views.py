from django.shortcuts import render
from rateYoCourse.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.ursresolvers import reverse
from datetime import datetime
# Create your views here.
# Itech team AB - if program won't run, comment out some of these views
def index(request):
  visit_cookie_handler(request)
	context_dict['visits'] = request.session['visits']
	
  response = render(request, 'rateyocourse/index.html', context=context_dict)
  return response

def get_server_side_cookie(request, cookie, default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val
	
def visitor_cookie_handler(request):
	visits = int(request.COOKIES.get('visits', 1))
	
	last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now())
	last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
	
	if (datetime.now() - last_visit_time).days > 0:
		visits = visits + 1
		request.session['last_visit'] = str(datetime.now())
	else:
		request.session['last_visit'] = last_visit_cookie
		
	request.session['visits'] = visits

def register(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			
			user.set_password(user.password)
			user.save()
			
			profile = profile_form.save(commit = False)
			profile.user = user
			
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
				
			profile.save()
			
			registered = True
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
		
	return render(request, 'rateyocourse/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
	
def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		pasword = request.POST.get('password')
		
		user = authenticate(username=username, password=password)
		
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
				
			else:
				return HttpResponse("Your account is disabled.")
				
		else:
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'rateyocourse/login.html', {})
				
@login_required 
def user_logout(request):
	logout(request)
	
	return HttpResponseRedirect(reverse('index'))
	
