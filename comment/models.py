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

    # ���ṹ��ʵ�����ۻظ�
    # �ظ��ĸ����,�����ȡ�����ظ��б������ֻ�ø��ڵ�ĵݹ����
    root = models.ForeignKey('self', related_name="root_comment", null=True, on_delete=models.CASCADE)
    # �ظ��ĸ��ڵ�
    parent = models.ForeignKey('self', related_name="parent_comment", null=True, on_delete=models.CASCADE)
    # ���ظ��Ķ���
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)

    class Meta:
        # ���۰�ʱ������
        ordering = ['comment_time']
