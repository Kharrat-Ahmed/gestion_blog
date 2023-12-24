# gestion_blog/apps.py

from django.apps import AppConfig

class GestionBlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_blog'
    verbose_name = 'Gestion de Blog'
