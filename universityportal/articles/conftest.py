import pytest
from django.test import RequestFactory
from mixer.backend.django import mixer


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def article(db):
    user = mixer.blend('auth.User')
    reviewer = mixer.blend('auth.User')
    return mixer.blend('articles.Articles', title="My Test Article", body="Sample description", user=user,
                       reviewer=reviewer)


@pytest.fixture
def comment(db, article):
    user = mixer.blend('auth.User')
    return mixer.blend('articles.Comment', article=article, author=user, text="This is test comment")