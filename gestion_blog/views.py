from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .forms import CommentForm, PostForm, LoginForm, EditProfileForm, ProfilePictureForm, MessageForm
from .models import Post, Like, Message
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count  # Add this import statement
from django.contrib.auth.models import User
from .models import Message



def home(request):
    return render(request, 'gestion_blog/home.html')
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(approved=True)

    # Check if the user has liked the post
    user_likes_post = False
    if request.user.is_authenticated:
        user_likes_post = Like.objects.filter(user=request.user, post=post).exists()

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

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'user_likes_post': user_likes_post,
    }

    return render(request, 'gestion_blog/post_detail.html', context)

import django.db.models as models

def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST' and request.user.is_authenticated:
        user = request.user

        # Check if the user has already liked the post
        like, created = Like.objects.get_or_create(user=user, post=post)

        if not created:
            like.delete()  # Unlike if already liked

        # Update post likes count using annotation
        post_with_likes = Post.objects.annotate(like_count=models.Count('like'))

        # Extract the like count for the specific post
        post_likes = post_with_likes.get(slug=slug).like_count

        return JsonResponse({'likes': post_likes, 'user_likes': not created})

    return JsonResponse({'error': 'User not authenticated'}, status=401)
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
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfilePictureForm(instance=request.user)
    return render(request, 'gestion_blog/profile.html', {'form': form})
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

def logout_view(request):
    logout(request)
    return render(request, 'gestion_blog/logout.html')  # Create a template for the logout confirmation

@login_required
def send_message(request, recipient_username):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            recipient = User.objects.get(username=recipient_username)

            # Create and save the message
            Message.objects.create(sender=request.user, recipient=recipient, content=content)

            return redirect('view_messages')  # Redirect to the view_messages page after sending the message
    else:
        form = MessageForm()

    context = {'form': form, 'recipient_username': recipient_username}
    return render(request, 'gestion_blog/send_message.html', context)
@login_required
def view_messages(request):
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    # Ajoutez ici la logique pour afficher les messages dans le modèle de messagerie
    return render(request, 'gestion_blog/view_messages.html', {'received_messages': received_messages,'sent_messages': sent_messages})
