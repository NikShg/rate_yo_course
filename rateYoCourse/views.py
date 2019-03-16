from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from rateYoCourse.forms import UserForm, UserProfileForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from rateYoCourse.models import UserProfile, University, Course
from rateYoCourse.models import Rate
from star_ratings.models import Rating
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
'''
#def login(request):
	#return render(request, 'login.html')
'''
@login_required
def home(request):
	return render(request, 'index.html')
'''
=======

>>>>>>> 7799bb623bcf7b24f064e0c7151e3c0bc24d3743
#def register(request):
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
<<<<<<< HEAD
'''
'''
=======


>>>>>>> 7799bb623bcf7b24f064e0c7151e3c0bc24d3743
#def user_login(request):
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
<<<<<<< HEAD
'''
'''
=======

>>>>>>> 7799bb623bcf7b24f064e0c7151e3c0bc24d3743
		#Commenting out as using registration app package
#@login_required
#def user_logout(request):
	logout(request)

	return HttpResponseRedirect(reverse('index'))
'''
# This function returns the view for the list of universities. Universities are fetched
# from the university table and sorted by name asscending.
def show_university_(request):
	context_dict = {}
	universities = University.objects.all().order_by('name')
	context_dict['universities'] = universities
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
	if request.method == 'POST':
		query = request.POST['query'].strip()

		if query:
			result_list = run_query(query)
			context_dict['query'] = query
			context_dict['result_list'] = result_list

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

def add_comment(request, slug):
	#university = get_object_or_404(University, slug=slug)
	#course = get_object_or_404(Course, slug=slug)
	university = University.objects.get(slug=university_name_slug)
	course = Course.objects.get(slug=course_name_slug)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment=form.save(commit=False)
			comment.course = course
			comment.save()
			return redirect('index') #this might have to be a uni slug

		else:
			form = CommentForm()
			template = 'rateyocourse/add_comment.html' #is this course or no course or just uni?
			content = {'form': form}
			return render(request, template, context)
'''
#@login_required
#def settings(request):
  #  user = request.user
    #try:
       # facebook_login = user.social_auth.get(provider='facebook')
    #except UserSocialAuth.DoesNotExist:
      #  facebook_login = None

    #can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    #return render(request, 'rateyocourse/settings.html', {
      #  'facebook_login': facebook_login,
       # 'can_disconnect': can_disconnect
    #})
	#
#@login_required
#def password(request):
 #   if request.user.has_usable_password():
   #     PasswordForm = PasswordChangeForm
    #else:
      #  PasswordForm = AdminPasswordChangeForm

    #if request.method == 'POST':
      #  form = PasswordForm(request.user, request.POST)
       # if form.is_valid():
         #   form.save()
          #  update_session_auth_hash(request, form.user)
            #messages.success(request, 'Your password was successfully updated!')
            #return redirect('password')
        #else:
          #  messages.error(request, 'Please correct the error below.')
    #else:
      #  form = PasswordForm(request.user)
#    return render(request, 'core/password.html', {'form': form})


'''
