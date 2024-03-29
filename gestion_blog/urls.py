# gestion_blog/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import register, profile, edit_profile, like_post, send_message, view_messages

urlpatterns = [
    path('', views.home, name='home'),
    path('post_list/', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('like/', like_post, name='like_post'),
    path('like/<slug:slug>/', like_post, name='like_post'),  # Make sure this line is included

    path('post/<slug:slug>/add-comment/', views.add_comment, name='add_comment'),
    path('add-post/', views.add_post, name='add_post'),
    path('login/', auth_views.LoginView.as_view(template_name='gestion_blog/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='gestion_blog/logout.html'), name='logout'),
    path('send_message/<str:recipient_username>/', send_message, name='send_message'),
    path('view_messages/', view_messages, name='view_messages'),


    # Add more URL patterns as needed for your app
]
