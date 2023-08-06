from rest_framework.fields import Field
from rest_framework.serializers import BaseSerializer
from wagtail.images.api.fields import ImageRenditionField
from django.conf import settings

def create_banner(page):
    banner = {}
    if hasattr(page, 'banner_title'):
        banner['title'] = page.banner_title
    if hasattr(page, 'banner_subtitle'):
        banner['subtitle'] = page.banner_subtitle
    if hasattr(page, 'banner_image'):
        spec = getattr(settings, 'IMAGE_BANNER_RENDERITION', 'fill-300x200')
        banner['image'] = ImageRenditionField(spec).to_representation(page.banner_image)
    return banner

def create_page(page):
    result = {
        'id': page.id,
        'slug': page.slug,
        'url': page.url,
        'last_published_at': page.last_published_at,
        'banner': create_banner(page),
    }
    if hasattr(page, 'keywords'):
        result['keywords'] =[tag.name for tag in page.keywords.all()]
    return result

class BanneredChildrenSerializer(Field):
    def to_representation(self, value):
        request = self.context['request']
        qs = value.specific()
        order = request.query_params.get('order', None)
        if order is not None:
            qs = qs.order_by(order)
        qs = self.context['view'].paginate_queryset(qs)
        for page in qs:
            yield create_page(page)

class RFBanneredChildrenSerializer(BaseSerializer):

    def to_representation(self, instance):
        return create_page(instance.specific)