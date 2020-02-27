# !/usr/bin/ env python
# coding=UTF-8
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse
from django.utils.timezone import localtime
from .models import Comment
from .forms import CommentForm
# Create your views here.


def update_comment(request):
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        # 检查通过，保存数据
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        # 判断是否有上一级评论
        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        # 利用JsonResponse将数据返回前端
        data['status'] = 'SUCCES'
        data['username'] = comment.user.get_nickname_or_username()
        data['comment_time'] = localtime(comment.comment_time).strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if parent is not None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root is not None else ''
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0]
    return JsonResponse(data)
