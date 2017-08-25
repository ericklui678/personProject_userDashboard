from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    admin_level = models.BooleanField(default=False)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Post(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, related_name="posts")
    wall = models.ForeignKey(User, related_name="wall")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, related_name="comments")
    post = models.ForeignKey(Post, related_name="comments")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
