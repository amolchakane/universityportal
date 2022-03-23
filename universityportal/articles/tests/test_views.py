from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer
from django.urls import reverse
import pytest
from django.test import RequestFactory
from articles.views import article_details


@pytest.mark.django_db
class TestViews:

    def test_article_detail_authenticated(self):
        user = mixer.blend('auth.User')
        reviewer = mixer.blend('auth.User')
        mixer.blend('articles.Articles', title="My Test Article", body="Sample description", user=user,
                    reviewer=reviewer)
        path = reverse("details", kwargs={'id': 1})
        request = RequestFactory().get(path)
        request.user = mixer.blend('auth.User')
        response = article_details(request, id=1)
        assert response.status_code == 200

    def test_article_detail_unauthenticated(self):
        user = mixer.blend('auth.User')
        reviewer = mixer.blend('auth.User')
        mixer.blend('articles.Articles', title="My Test Article", body="Sample description", user=user,
                    reviewer=reviewer)
        path = reverse("details", kwargs={'id': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = article_details(request, id=1)
        assert response.status_code == 302
        assert 'accounts/login' in response.url
