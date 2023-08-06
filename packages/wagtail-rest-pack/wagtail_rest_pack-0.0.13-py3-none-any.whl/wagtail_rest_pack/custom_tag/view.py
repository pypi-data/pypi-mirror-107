from rest_framework import generics
from rest_framework import serializers

from .models import PageTag


class TagSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField()
    class Meta:
        model = PageTag
        fields = ['tag']


class TagViewset(generics.ListAPIView):
    model = PageTag
    queryset = PageTag.objects.all() # todo lists all tags, I need a set, no duplicates plase :)
    serializer_class = TagSerializer
