from django.urls import reverse
from mixer.backend.django import mixer

from articles.views import article_details


def test_article_creation(factory, article):
    """Test to validate Article creation
    factory: RequestFactory object from fixture
    article: Article object from fixture
    """
    path = reverse("details", kwargs={'id': 1})
    request = factory.get(path)
    request.user = mixer.blend('auth.User')
    response = article_details(request, id=1)
    assert response.status_code == 200
    assert article.title == "My Test Article"


def test_article_creation_default_status_is_pending(article):
    """Test to validate Article default status is pending
    article: Article object from fixture
    """
    assert article.status == 'pending'


def test_comment_adding(comment):
    """Test to validate comment adding feature"""
    assert comment.text == "This is test comment"

