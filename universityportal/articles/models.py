from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Articles(models.Model):
    """Article Model comprises of following fields
    title: Title of the Article
    body: Description of the Article
    created_at: The date when article was created
    user: The owner of the Article
    reviewer: To which user the article was assigned for review
    status: Status of the Article (pending/approved)
    """
    title = models.CharField(max_length=200)
    body = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, related_name='reviewer', null=True, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, default='pending')


class UserRoles(models.Model):
    """UserRoles model
    Stores 'student' and 'professor' role of the user
    """
    role = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Comment(models.Model):
    """Comments model
    Stores the comments added on Article
    """
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


