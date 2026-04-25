from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializer
from .forms import NewUserForm, CommentForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import logging
import datetime

logger = logging.getLogger(__name__)

class PostList(generic.ListView):
	queryset = Post.objects.filter(status=1).order_by('-created_on')
	template_name = 'index.html'

	def get(self, request, *args, **kwargs):
		# 3. Записываем сообщение в лог
		logger.warning(f'Homepage was accessed at {datetime.datetime.now()} hours!')
		return super().get(request, *args, **kwargs)

def post_detail(request, slug):
	post = get_object_or_404(Post, slug=slug)
	comments = post.comments.all()
	if request.method == 'POST' and request.user.is_authenticated:
		cf = CommentForm(request.POST)
		if cf.is_valid():
			c = cf.save(commit=False)
			c.post, c.user = post, request.user
			c.save()
			return redirect('post_detail', slug=slug)
	return render(request, 'post_detail.html', {'post':post, 'comments':comments, 'comment_form':CommentForm()})

class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			login(request, form.save())
			return redirect("home")
	return render(request, "app/register.html", {"register_form": NewUserForm()})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
			if user:
				login(request, user)
				return redirect("home")
	return render(request, "app/login_auth.html", {"login_form": AuthenticationForm()})

def logout_request(request):
	logout(request)
	return redirect("home")

def cookie_session(request):
	request.session.set_test_cookie()
	return HttpResponse("<h1>dataflair</h1><p>Test cookie set!</p>")

def cookie_delete(request):
	if request.session.test_cookie_worked():
		request.session.delete_test_cookie()
		response = HttpResponse("dataflair<br> cookie created and then deleted")
	else:
		response = HttpResponse("Dataflair <br> Your browser does not accept cookies")
	return response

# --- Создание и доступ к сессиям (стр. 8-12 PDF) ---
def create_session(request):
	request.session['name'] = 'username'
	request.session['password'] = 'password123'
	return HttpResponse("<h1>dataflair<br> the session is set</h1>")

def access_session(request):
	response = "<h1>Welcome to Sessions of dataflair</h1><br>"
	if request.session.get('name'):
		response += "Name : {0} <br>".format(request.session.get('name'))
		if request.session.get('password'):
			response += "Password : {0} <br>".format(request.session.get('password'))
		return HttpResponse(response)
	else:
		# Если сессии нет, перенаправляем на создание (стр. 9 PDF)
		return redirect('create_session_url')

def delete_session(request):
	try:
		if 'name' in request.session:
			del request.session['name']
		if 'password' in request.session:
			del request.session['password']
	except KeyError:
		pass
	return HttpResponse("<h1>dataflair<br>Session Data cleared</h1>")