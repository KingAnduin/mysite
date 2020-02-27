from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)

    # 树结构来实现评论回复
    # 回复的根结点,方便获取整个回复列表，避免的只用父节点的递归操作
    root = models.ForeignKey('self', related_name="root_comment", null=True, on_delete=models.CASCADE)
    # 回复的父节点
    parent = models.ForeignKey('self', related_name="parent_comment", null=True, on_delete=models.CASCADE)
    # 被回复的对象
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)

    class Meta:
        # 评论按时间排列
        ordering = ['comment_time']
