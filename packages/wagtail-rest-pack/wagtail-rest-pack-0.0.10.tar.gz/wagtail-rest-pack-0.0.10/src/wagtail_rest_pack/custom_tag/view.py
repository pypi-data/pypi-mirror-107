from wagtail.api.v2.utils import BadRequestError
from wagtail.api.v2.views import BaseAPIViewSet
from wagtail.core.models import Page

from wagtail_rest_pack.page_banner.serializers import RFBanneredChildrenSerializer
# from .models import PageTag
from taggit.models import TaggedItemBase

class FakeModel:
    pass

class ObjectsByTagViewset(BaseAPIViewSet):
    known_query_parameters = BaseAPIViewSet.known_query_parameters.union(['with_tags'])
    model = FakeModel

    def listing_view(self, request):
        return super(ObjectsByTagViewset, self).listing_view(request)

    def get_serializer_class(self):
        return RFBanneredChildrenSerializer

    def get_queryset(self):
        tags = self.request.query_params.get('with_tags', '').split(',')
        if not tags:
            raise BadRequestError('Query paramater `s` must be provided')
        if len(tags) > 5:
            raise BadRequestError('Only 5 tags at once are allowed')
        return Page.objects.filter(id__in=TaggedItemBase.objects.filter(tag__name__in=tags).values_list('content_object'))
