from django.db import models
from django.db.models.fields import exceptions
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNum, ReadNumExpandMethod, ReadDetail


# superuser 姓名全拼/～123


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 反向关联ReadDetail模型
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog: %s>" % self.title

    # 按创建时间排序，使用分页器前需先排序
    class Meta:
        ordering = ['-created_time']

