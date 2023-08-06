from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.core.models import Page
from wagtail.snippets.models import register_snippet
from taggit.models import Tag as TaggitTag
from django.utils.translation import gettext_lazy as _


@register_snippet
class Tag(TaggitTag):
    class Meta:
        verbose_name = _('Keyword')
        verbose_name_plural = _('Keywords')
        proxy = True


class PageTag(TaggedItemBase):
    content_object = ParentalKey(
        Page,
        related_name='tagged_pages',
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = 'wagtail_rest_pack'
