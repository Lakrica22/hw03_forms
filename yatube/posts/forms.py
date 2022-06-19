from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post

class PostForm(forms.ModelForm):
    
    class Meta(UserCreationForm.Meta):
        model = Post
        fields = ['text', 'group']
