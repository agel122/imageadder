from django import forms
from .models import PostedPicture


class PostImage(forms.ModelForm):
    class Meta:
        model = PostedPicture
        fields = ['title', 'cover']
