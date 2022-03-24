import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from articles.views import article_details


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def article(db):
    user = mixer.blend('auth.User')
    reviewer = mixer.blend('auth.User')
    return mixer.blend('articles.Articles', title="My Test Article", body="Sample description", user=user,
                       reviewer=reviewer)


def test_article_detail_authenticated(factory, article):
    path = reverse("details", kwargs={'id': 1})
    request = factory.get(path)
    request.user = mixer.blend('auth.User')
    response = article_details(request, id=1)
    assert response.status_code == 200


def test_article_detail_unauthenticated(factory, article):
    path = reverse("details", kwargs={'id': 1})
    request = factory.get(path)
    request.user = AnonymousUser()
    response = article_details(request, id=1)
    assert response.status_code == 302
    assert 'accounts/login' in response.url
