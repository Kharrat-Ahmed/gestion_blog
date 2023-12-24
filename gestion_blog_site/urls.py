# gestion_blog_site/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion_blog.urls')),  # Include the URLs of gestion_blog app
]

