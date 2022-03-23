from rest_framework import serializers
from .models import Articles


class ArticleSerializer(serializers.ModelSerializer):
    model = Articles
    fields = ["id", "title", "body", "created_at", "user", "reviewer", "status"]
