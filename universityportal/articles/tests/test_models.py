from django.urls import reverse
from mixer.backend.django import mixer

from articles.views import article_details


def test_article_creation(factory, article):
    path = reverse("details", kwargs={'id': 1})
    request = factory.get(path)
    request.user = mixer.blend('auth.User')
    response = article_details(request, id=1)
    assert response.status_code == 200
    assert article.title == "My Test Article"


def test_article_creation_default_status_is_pending(article):
    assert article.status == 'pending'


def test_comment_adding(comment):
    assert comment.text == "This is test comment"

