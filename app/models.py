# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Post(models.Model):
    text = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} created by {} at {}".format(self.text, self.created_by.username, self.created_at)

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    birthday = models.DateField(blank=True)
    friend_requests = models.ManyToManyField(User, related_name='friend_requests', blank=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
