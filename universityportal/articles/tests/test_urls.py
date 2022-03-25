from django.urls import reverse, resolve


def test_article_detail_url():
    """Test to check article detail URL"""
    path = reverse("details", kwargs={'id': 1})
    assert resolve(path).view_name == "details"
