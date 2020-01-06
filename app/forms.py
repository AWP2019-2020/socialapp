from django import forms
from app import models


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['text']


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['text', 'image']


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    e_mail = forms.CharField(max_length=100)
    class Meta:
        model = models.UserProfile
        exclude = ['user', 'friend_requests', 'friends']
