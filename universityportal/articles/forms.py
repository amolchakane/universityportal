from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Articles, Comment


class NewUserForm(UserCreationForm):
    """New user registration form"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ArticleForm(forms.ModelForm):
    """Article creation form"""
    class Meta:
        model = Articles
        fields = ('title', 'body',)


class CommentForm(forms.ModelForm):
    """Form for adding comment"""
    class Meta:
        model = Comment
        fields = ('text',)



