from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from rateYoCourse.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from rateYoCourse.models import UserProfile, University, Course


# Create your views here.
# Itech team AB - if program won't run, comment out some of these views
def index(request):
	context_dict = {}
	visitor_cookie_handler(request)


	context_dict['visits'] = request.session['visits']

	response = render(request, 'rateyocourse/index.html', context=context_dict)
	return response

def about(request):
	visitor_cookie_handler(request)
	context_dict = {}
	context_dict['visits'] = request.session['visits']
	response = render(request, 'rateyocourse/about.html', context_dict)
	return response

def get_server_side_cookie(request, cookie, default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val

def visitor_cookie_handler(request):
	visits = int(get_server_side_cookie(request,'visits', '1'))
	last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
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
			user.set_password(user.password)
			user.save()
			
			profile = profile_form.save(commit=False)
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
		password = request.POST.get('password')

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

def show_university_(request):
	context_dict = {}
	universities = University.objects.all()
	#'university_names = University.objects.get(slug=university_name_slug)
	context_dict['universities'] = universities
	#context_dict['university_names'] = university_names
	return render(request, 'rateYoCourse/universities.html', context=context_dict)

	
def show_university(request, university_name_slug):
	context_dict = {}
	
	try:
		university = University.objects.get(slug=university_name_slug)
		courses = Course.objects.filter(university=university)
		context_dict['courses'] = courses
		context_dict['university'] = university
	except:
		context_dict['university'] = None
		context_dict['courses'] = None
	#context_dict = {'boldmessage': "Here will be all the info you need!"}
	return render(request, 'rateYoCourse/university.html', context=context_dict)

def show_course(request, university_name_slug, course_name_slug):
	context_dict = {}
	try:
		university = University.objects.get(slug=university_name_slug)
		course = Course.objects.get(slug=course_name_slug)
		context_dict['course'] = course
		context_dict['university'] = university
	except:
		context_dict['course'] = None
		context_dict['university'] = None
	#context_dict = {'boldmessage': "Here will be all the info you need!"}

	return render(request, 'rateYoCourse/course.html', context=context_dict)


@login_required
def register_profile(request):
	form = UserProfileForm()
	
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES)
		if form.is_valid():
			user_profile = form.save(commit=False)
			user_profile.user = request.user
			user_profile.save()
			
			return redirect('index')
		else:
			print(form.errors)
			
	context_dict = {'form': form}
	
	return render(request, 'rateyocourse/profile_registration.html', context_dict)

@login_required
def profile(request, username):
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return redirect('index')
		
	userprofile = UserProfile.objects.get_or_create(user=user)[0]
	form = UserProfileForm({'picture': userprofile.picture})
	
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
		if form.is_valid():
			form.save(commit=True)
			return redirect('profile', user.username)
		else:
			print(form.errors)
	
	return render(request, 'rateyocourse/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})
	
@login_required
def list_profiles(request):
	userprofile_list = UserProfile.objects.all()
	
	return render(request, 'rateyocourse/list_profiles.html', {'userprofile_list': userprofile_list})

