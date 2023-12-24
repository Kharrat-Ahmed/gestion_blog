# gestion_blog_site/urls.py

from django.contrib import admin
from django.urls import path, include


##app_name = 'gestion_blog'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion_blog.urls')),

]

