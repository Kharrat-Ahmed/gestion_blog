# gestion_blog/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import register

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/add-comment/', views.add_comment, name='add_comment'),
    path('add-post/', views.add_post, name='add_post'),
    path('login/', auth_views.LoginView.as_view(template_name='gestion_blog/login.html'), name='login'),
    path('register/', views.register, name='register'),

    # Add more URL patterns as needed for your app
]