from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializer
from .forms import NewUserForm, CommentForm

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

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