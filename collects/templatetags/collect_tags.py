from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import CollectCount, CollectRecord


register = template.Library()

@register.simple_tag
def get_collect_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    collect_count, created = CollectCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    if collect_count.collect_num == 0 and str(content_type) == 'comment | comment':
        return ''
    else:
        return collect_count.collect_num

@register.simple_tag(takes_context=True)
def get_collect_status(context, obj):
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if CollectRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''

@register.simple_tag
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model
