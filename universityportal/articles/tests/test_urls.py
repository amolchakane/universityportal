from django.urls import reverse, resolve


class TestUrls:

    def test_article_detail_url(self):
        path = reverse("details", kwargs={'id': 1})
        assert resolve(path).view_name == "details"
