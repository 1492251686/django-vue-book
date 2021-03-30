from rest_framework import serializers
from .models import BookSource


class BookSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSource
        fields = ['id', 'name']