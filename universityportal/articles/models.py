from asyncio.windows_events import NULL
from tkinter import CASCADE
from django.conf import settings
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


# Create your models here.
class Articles(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, related_name='reviewer', null=True, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, default='pending')


class UserRoles(models.Model):
    role = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Comment(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


