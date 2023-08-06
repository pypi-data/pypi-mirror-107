from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Comment(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, on_delete=models.SET_NULL, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now_add=False, default=None, null=True, editable=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_by')
    body = models.TextField(max_length=2000)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id', for_concrete_model=False)

    class Meta:
        ordering = ['created_on', 'created_by']

    @property
    def is_staff(self):
        if self.created_by is not None:
            return self.created_by.is_staff
        return False

    @property
    def name(self):
        if self.created_by is not None and self.created_by.is_active:
            return self.created_by.username
        return None

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
