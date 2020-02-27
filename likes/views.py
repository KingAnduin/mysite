# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from datetime import datetime
from .models import LikeCount, LikeRecord
# Create your views here.


def succes_response(like_num):
    data = {}
    data['status'] = 'SUCCES'
    data['liked_num'] = like_num
    return JsonResponse(data)


def error_response(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def like_change(request):
    # 获取数据
    user = request.user
    if not user.is_authenticated:
        return error_response(400, '您还没有登录')

    content_type = request.GET.get('content_type')  # get获得的只是一个字符串
    object_id = request.GET.get('object_id')
    # 验证被点赞的对象是否存在
    try:
        content_type = ContentType.objects.get(model=content_type)  # 此时才获得ContentType
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return error_response(401, '点赞对象不存在')

    # 处理数据
    if request.GET.get('is_like') == 'true':
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 未点赞，进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return succes_response(like_count.liked_num)
            pass
        else:
            # 已点赞过，不能重复点赞(一个用户对同一个对象只能点赞一次)
            return error_response(402, '已点赞过，不能重复点赞')
    else:
        # 取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有点赞过，则取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            # 点赞总数减一
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return succes_response(like_count.liked_num)
            else:
                return error_response(403, '数据错误')
        else:
            # 没有点赞过，不能取消
            return error_response(404, '未点赞过，不能取消点赞')
