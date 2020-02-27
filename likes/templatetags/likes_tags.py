from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount, LikeRecord


# 模版标签
register = template.Library()


# 获取某个类型对象的评论总数
@register.simple_tag
def get_like_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    return like_count.liked_num


# 判断是否已经点赞
@register.simple_tag(takes_context=True)
def get_like_status(context, obj):
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if LikeRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''


@register.simple_tag()
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model
