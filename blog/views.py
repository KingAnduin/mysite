# -*- coding:utf-8 -*-
from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator
from django.db.models import Count
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from comment.forms import CommentForm
from user.forms import LoginForm


def get_blog_list_common_data(request, blos_all_list):
    # 每10篇进行分页
    paginator = Paginator(blos_all_list, settings.EACH_PAGE_BLOG_NUMBER)
    # 获取url页面参数（GET）
    page_num = request.GET.get('page', 1)
    # 获取分页器对应页码的博客信息
    page_of_blogs = paginator.get_page(page_num)
    # 获取当前页码
    current_page_num = page_of_blogs.number
    # 获取当前页邻近页的页码
    page_range = [x for x in range(int(current_page_num) - 2, int(current_page_num) + 3) if
                  0 < x <= paginator.num_pages]
    # 添加省略页标识
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 添加首页和尾页页码
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    # dates:按年月分类
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order='DESC')
    context['page_of_blogs'] = page_of_blogs
    context['blogs'] = page_of_blogs.object_list
    context['blogs_count'] = Blog.objects.all().count()
    # annotate: Django组合查询 = Group By
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['page_range'] = page_range
    return context


# 文章列表
def blog_list(request):
    blos_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blos_all_list)
    return render(request, 'blog/blog_list.html', context)


# 文章分类
def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blos_all_list = Blog.objects.filter(blog_type=blog_type)

    context = get_blog_list_common_data(request, blos_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)


# 博客按年月分类展示
def blogs_with_date(request, year, month):
    blos_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)

    context = get_blog_list_common_data(request, blos_all_list)
    context['blogs_with_dates'] = ' %s-%s ' % (year, month)
    return render(request, 'blog/blogs_with_date.html', context)


# 文章详情
def blog_detail(request, blog_pk):
    context = {}
    # pk = urls.py中对应的path名称
    blog = get_object_or_404(Blog, pk=blog_pk)
    # 记录阅读量
    read_cookie_key = read_statistics_once_read(request, blog)
    # 评论对象
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk, parent=None)

    context['blog'] = blog
    context['user'] = request.user
    context['comments'] = comments.order_by('-comment_time')
    # form表单
    context['comment_form'] = CommentForm(initial={'content_type': blog_content_type.model, 'object_id': blog_pk, 'reply_comment_id': 0})
    context['login_form'] = LoginForm()
    # 获取比当前blog创建时间晚的博客集合中最后一条
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    # 获取比当前blog创建时间早的博客集合中第一条
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    # 设置cookie用于记录阅读量
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')
    return response
