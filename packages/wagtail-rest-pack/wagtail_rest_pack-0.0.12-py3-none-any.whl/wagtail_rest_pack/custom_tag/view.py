from wagtail.api.v2.utils import BadRequestError
from wagtail.api.v2.views import BaseAPIViewSet
from wagtail.core.models import Page
from rest_framework import generics
from .models import PageTag
from rest_framework import serializers

class TagSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField()
    class Meta:
        model = PageTag
        fields = ['tag']


class TagViewset(generics.ListAPIView):
    model = PageTag
    queryset = PageTag.objects.all() # todo lists all tags, I need a set, no duplicates plase :)
    serializer_class = TagSerializer
