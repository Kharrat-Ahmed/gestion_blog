# gestion_blog/forms.py

from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'slug']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())