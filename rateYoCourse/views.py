from __future__ import unicode_literals
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
from rateYoCourse.models import Rate
from star_ratings.models import Rating, UserRating
from django.views.generic import DetailView, TemplateView
from django.shortcuts import redirect
from django.db.models import Q

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

# This function returns the view for the list of universities. Universities are fetched
# from the university table and sorted by name asscending.
def show_university_(request):
	context_dict = {}
	try:
		universities = University.objects.all().order_by('name')[:5]
		course_ratings = Rating.objects.filter(content_type = 8).order_by('-average')
		university_ratings = Rating.objects.filter(content_type = 9).order_by('-average')
		userratings = UserRating.objects.all().order_by('rating')[:5] ## top 5 most recent user ratings
		courses = Course.objects.all().order_by('name')[:5]
		context_dict['universities'] = universities
		context_dict['userratings'] = userratings
		context_dict['courses']= courses
		context_dict['course_ratings']= course_ratings
		context_dict['university_ratings']= university_ratings
	except:
		context_dict['universities'] = None
		context_dict['userratings'] = None
		context_dict['courses']= None
		context_dict['course_ratings']= None
		context_dict['university_ratings']= None
	return render(request, 'rateYoCourse/universities.html', context=context_dict)

# This function returns the view for the list of courses provided by a university. #
# A selection of courses are fetched depending on the selected university and sorted in ascending order.
def show_university(request, university_name_slug):
	context_dict = {}

	try:
		university = University.objects.get(slug=university_name_slug)
		courses = Course.objects.filter(university=university).order_by('name')
		context_dict['courses'] = courses
		context_dict['university'] = university
	except:
		context_dict['university'] = None
		context_dict['courses'] = None
	return render(request, 'rateYoCourse/university.html', context=context_dict)

# This view defines method that returns the information for a particular course provided by a particular university
def show_course(request, university_name_slug, course_name_slug):
	context_dict = {}
	try:
		university = University.objects.get(slug=university_name_slug)
		course = Course.objects.get(slug=course_name_slug)
		context_dict['course'] = course
		context_dict['university'] = university
	except Course.DoesNotExist:
		context_dict['course'] = None
		context_dict['university'] = None

	context_dict['query'] = course.name
	result_list = []

	return render(request, 'rateYoCourse/course.html', context=context_dict)

class RateView(DetailView):
    model = Rate

    def get_object(self, queryset=None):
        obj, created = self.model.objects.get_or_create(bar='rate bar baz')
        return obj


class SizesView(TemplateView):
    model = Rate
    template_name = 'sizes.html'

    def get_context_data(self, **kwargs):
        kwargs['sizes'] = {size: self.model.objects.get_or_create(bar=str(size))[0] for size in range(10, 40)}
        return super(SizesView, self).get_context_data(**kwargs)


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
	form = UserProfileForm({'picture': userprofile.picture, 'about': userprofile.about, 'status': userprofile.status})

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
	
def track_url(request):
	course_id = None
	url = '/rateyocourse/'
	if request.method == 'GET':
		if 'course_id' in request.GET:
			course_id= request.GET['course_id']
			try:
				course = Course.objects.get(id=course_id)
				course.views = Course.views + 1
				course.save()
				url = course.url
			except:
				pass
	return redirect(url)


def search(request):
	error = False
	if'q' in request.GET:
		q = request.GET['q']
		if not q:
			error = True
		else:
			course = Course.objects.filter(name__icontains = q)
			university = University.objects.filter(name__icontains = q)
			return render(request, 'rateyocourse/search_results.html', {'universities':university, 'courses':course,'query': q})


	return render(request, 'rateyocourse/search_form.html',{'error':error})