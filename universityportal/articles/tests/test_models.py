import pytest
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from articles.views import article_details


@pytest.mark.django_db
class TestArticles:

    def test_article_creation(self):
        user = mixer.blend('auth.User')
        reviewer = mixer.blend('auth.User')
        mixer.blend('articles.Articles', title="My Test Article", body="Sample description", user=user,
                    reviewer=reviewer)
        path = reverse("details", kwargs={'id': 1})
        request = RequestFactory().get(path)
        request.user = mixer.blend('auth.User')
        response = article_details(request, id=1)
        assert response.status_code == 200
