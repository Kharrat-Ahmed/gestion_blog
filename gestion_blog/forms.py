# gestion_blog/forms.py

from django import forms
from .models import Post, Comment, CustomUser
from django.contrib.auth.forms import UserChangeForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'slug']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

class EditProfileForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize labels, widgets, etc., if needed
        # For example:
        # self.fields['username'].label = 'New Username'    