import pytest
from django.test import RequestFactory
from mixer.backend.django import mixer


@pytest.fixture
def factory():
    """Return RequestFactory object"""
    return RequestFactory()


@pytest.fixture
def article(db):
    """Creates a article using mixer package"""
    user = mixer.blend('auth.User')
    reviewer = mixer.blend('auth.User')
    return mixer.blend('articles.Articles', title="My Test Article", body="Sample description", user=user,
                       reviewer=reviewer)


@pytest.fixture
def comment(db, article):
    """Creates a comment using mixer package"""
    user = mixer.blend('auth.User')
    return mixer.blend('articles.Comment', article=article, author=user, text="This is test comment")
