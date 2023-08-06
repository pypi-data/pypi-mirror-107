from rest_framework import generics
from rest_framework.fields import SerializerMethodField
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer
from wagtail_rest_pack.exception.handler import custom_exception_handler

from wagtail_rest_pack.comments.content_type import create_content_type_id
from wagtail_rest_pack.comments.models import Comment


class GetCommentSerializer(ModelSerializer):
    children = SerializerMethodField('_get_children')

    class Meta:
        model = Comment
        fields = ['id', 'is_staff', 'name', 'parent', 'created_on', 'created_by', 'updated_on', 'updated_by', 'body',
                  'children']

    def _get_children(self, obj):
        children = Comment.objects.filter(parent_id=obj.id).order_by('created_on')
        serializer = GetCommentSerializer(children, many=True)
        return serializer.data


class ListCommentAPIView(generics.ListAPIView):
    """
    example: /?content_type=wagtailcore.Page&object_id=4
    """
    permission_classes = [AllowAny]
    serializer_class = GetCommentSerializer

    def get_queryset(self):
        object_id = self.request.query_params.get('object_id', None)
        content_type = self.request.query_params.get('content_type', None)
        content_type_id = create_content_type_id(object_id, content_type)
        return Comment.objects.filter(object_id=object_id, content_type_id=content_type_id, parent=None)

    def get_exception_handler(self):
        return custom_exception_handler
