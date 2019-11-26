from django import forms
from app import models


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['text']


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['text']
