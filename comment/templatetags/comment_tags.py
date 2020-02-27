from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment


# 模版标签
register = template.Library()


# 获取某个类型对象的评论总数
@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()
