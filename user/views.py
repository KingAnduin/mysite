# -*- coding:utf-8 -*-
import datetime
import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from .forms import LoginForm, RegForm, ChangeNicknameForm, BindEmailForm
from .models import Profile


# 用户登录
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            # 用户成功登陆则重定向到之前的地址
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)


# 用户表单登录
def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    # 直接返回data无法解析
    return JsonResponse(data)


# 注册
def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = reg_form.cleaned_data['email']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 登陆用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context)


# 用户登出
def logout(request):
    auth.logout(request)
    # 返回当前页面
    return redirect(request.GET.get('from', reverse('home')))


# 用户信息
def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)


# 修改昵称
def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()
    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = form
    # 返回url
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)


# 绑定邮箱
def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(redirect_to)
    else:
        form = BindEmailForm()
    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    # 返回url
    context['return_back_url'] = redirect_to
    return render(request, 'user/bind_email.html', context)


# 发送验证码
def send_verification_code(request):
    data = {}
    email = request.GET.get('email', '')
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        # 根据时间判断是否发送邮件
        now_time = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now_time-send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            # 发送邮件
            request.session['bind_email_code'] = code
            request.session['send_code_time'] = send_code_time
            send_mail(
                '绑定邮箱',
                '验证码: %s' % code,
                'hanjiangong.swust@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)
