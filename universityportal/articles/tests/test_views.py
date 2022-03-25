from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from mixer.backend.django import mixer

from articles.views import article_details


def test_article_detail_authenticated(factory, article):
    """Test to check if Article details are allowed
    only to access to logged in users
    """
    path = reverse("details", kwargs={'id': 1})
    request = factory.get(path)
    request.user = mixer.blend('auth.User')
    response = article_details(request, id=1)
    assert response.status_code == 200


def test_article_detail_unauthenticated(factory):
    """Test to check if Article details access is
    not allowed to non logged in users
    """
    path = reverse("details", kwargs={'id': 1})
    request = factory.get(path)
    request.user = AnonymousUser()
    response = article_details(request, id=1)
    assert response.status_code == 302
    assert 'accounts/login' in response.url
