from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .forms import CommentForm, PostForm, LoginForm, EditProfileForm
from .models import Post
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(approved=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user  # Assuming you have user authentication
            new_comment.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()

    return render(request, 'gestion_blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})

def post_list(request):
    # Retrieve all posts from the database
    posts = Post.objects.all()

    # Generate a dictionary to store comment URLs for each post
    comment_urls = {}

    # Loop through each post and generate the comment URL
    for post in posts:
        # Check if the post has a valid slug before generating the URL
        if post.slug:
            comment_urls[post.slug] = reverse('add_comment', kwargs={'slug': post.slug})

    # Include comment_urls in the context
    context = {'posts': posts, 'comment_urls': comment_urls}

    return render(request, 'gestion_blog/post_list.html', context)

def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user  # Assuming you have user authentication
            new_comment.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()

    return render(request, 'gestion_blog/add_comment.html', {'form': form, 'post': post})
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user  # Assuming you have user authentication
            new_post.save()
            return redirect('post_list')
    else:
        form = PostForm()

    return render(request, 'gestion_blog/add_post.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirect to post_list upon successful login
                return redirect('post_list')
            else:
                # Handle invalid login credentials
                form.add_error(None, 'Invalid login credentials. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'gestion_blog/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Redirect to the home page after registration
    else:
        form = UserCreationForm()

    return render(request, 'gestion_blog/register.html', {'form': form})
def profile(request):
    # Add logic to fetch and display user profile information
    return render(request, 'gestion_blog/profile.html')
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'gestion_blog/edit_profile.html', {'form': form})