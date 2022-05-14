import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.conf import settings
from django.utils import timezone
from django.db.models import Count
from blog.models import Blog, BlogType
from reply_card.models import ReplyCard, MessageNum
from collects.models import CollectRecord
from .forms import LoginForm, RegForm, ChangeNicknameForm, ChangeEmailForm, ChangePasswordForm, ForgotPasswordForm, DelReplyCardForm, DelBlogForm, DelCollectForm
from .models import Profile



def login(request):
    context = {}
    context['login_form'] = LoginForm
    context['reg_form'] = RegForm
    return render(request, 'user/login.html', context)

def register(request):

    context = {}
    context['reg_form'] = RegForm
    context['login_form'] = LoginForm
    return render(request, 'user/register.html', context)

def login_form(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def register_form(request):
    data = {}
    reg_form = RegForm(request.POST, request=request)
    if reg_form.is_valid():
        username = reg_form.cleaned_data['username']
        email = reg_form.cleaned_data['email']
        password = reg_form.cleaned_data['password']
        # 创建用户
        user = User.objects.create_user(username, email, password)
        user.save()
        # 清除seession
        del request.session['register_code']
        # 登录用户
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        reg_form = RegForm(request.POST, request=request)
        data['msg'] = reg_form.errors
        data['status'] = 'ERROR'

    return JsonResponse(data)

def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))

def user_profile(request):


    context = {}

    if request.user.is_authenticated:
        user = request.user
        reply_card = ReplyCard.objects.filter(user=user)
        message_num = MessageNum.objects.filter(user=user)
        context['reply_cards'] = reply_card
        context['reply_card_del_from'] = DelReplyCardForm
        context['messages_num'] = message_num
        blogs = Blog.objects.filter(author=user)
        # 分页器
        page_num = request.GET.get('page', 1)
        paginator = Paginator(blogs, settings.EACH_PAGE_BLOG_NUMBER)
        page_of_blogs = paginator.get_page(page_num)
        currentr_page_num = page_of_blogs.number
        page_range = [x for x in range(currentr_page_num - 2, currentr_page_num + 3) if
                      x > 0 and x <= paginator.page_range[-1]]

        if page_range[0] - 1 >= 2:
            page_range.insert(0, "...")
        if paginator.num_pages - page_range[-1] >= 2:
            page_range.append("...")

        if page_range[0] != 1:
            page_range.insert(0, 1)
        if page_range[-1] != paginator.num_pages:
            page_range.append(paginator.num_pages)

        context['blogs'] = page_of_blogs.object_list
        context['blogs_manage'] = Blog.objects.filter(author=user)
        context['blog_del_form'] = DelBlogForm
        context['collects'] = CollectRecord.objects.filter(user=user)
        context['collect_del_form'] = DelCollectForm
        context['blog_count'] = Blog.objects.filter(author=user).count()
        context['page_range'] = page_range
        context['page_of_blogs'] = page_of_blogs
    return render(request, 'user/user_profile.html', context)

def reply_card_del(request):
    del_reply_card_form = DelReplyCardForm(request.POST)
    data = {}
    if del_reply_card_form.is_valid():
        num = del_reply_card_form.cleaned_data['num']
        reply_card = ReplyCard.objects.filter(id=num)
        reply_card.delete()
        data['status'] = 'SUCCESS'

    else:
        data['status'] = 'ERROR'

    return JsonResponse(data)

def reply_url(request):
    blog_id = request.GET.get('from', '')
    return redirect(reverse('home') + 'blog/' + str(blog_id))

def clear_message_num(request):
    data = {}
    if request.user.is_authenticated:
        user = request.user
        messagenum = MessageNum.objects.get(user=user)
        messagenum.num = 0
        messagenum.save()
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'

    return JsonResponse(data)

def blog_del(request):
    del_blog_form = DelBlogForm(request.POST)
    data = {}
    if del_blog_form.is_valid():
        blog_id = del_blog_form.cleaned_data['blog_id']
        blog = Blog.objects.get(id=blog_id)
        if request.user != blog.author:
            data['status'] = 'ERROR'
        else:
            blog.delete()
            data['status'] = 'SUCCESS'

    return JsonResponse(data)

def collect_del(request):
    del_collect_form = DelCollectForm(request.POST)
    data = {}
    if del_collect_form.is_valid():
        collect_record_id = del_collect_form.cleaned_data['collect_record_id']
        collect_record = CollectRecord.objects.filter(id=collect_record_id)
        if request.user != collect_record.user:
            data['status'] = 'ERROR'
        else:
            collect_record.delete()
            data['status'] = 'SUCCESS'

    return JsonResponse(data)


def user_info(request):

    context = {}
    context['change_nickname_form'] = ChangeNicknameForm
    context['change_email_form'] = ChangeEmailForm
    context['change_password_form'] = ChangePasswordForm
    context['forgot_password_form'] = ForgotPasswordForm
    context['blog_types'] = BlogType.objects.all()
    return render(request, 'user/user_info.html', context)

def change_nickname(request):
    change_nickname_form = ChangeNicknameForm(request.POST, user=request.user)
    data = {}
    if change_nickname_form.is_valid():
        nickname_new = change_nickname_form.cleaned_data['nickname_new']
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.nickname = nickname_new
        profile.save()
        data['status'] = 'SUCCESS'
        data['nickname'] = profile.nickname
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def change_email(request):
    change_email_form = ChangeEmailForm(request.POST, request=request)
    data = {}
    if change_email_form.is_valid():
        email = change_email_form.cleaned_data['email']
        request.user.email = email
        request.user.save()
        # 清除seession
        del request.session['change_email_code']

        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
        change_email_form = ChangeEmailForm(request.POST, request=request)
        data['msg'] = change_email_form.errors
    return JsonResponse(data)

def change_password(request):
    change_password_form = ChangePasswordForm(request.POST, user=request.user)
    data = {}
    if change_password_form.is_valid():
        user = request.user
        new_password = change_password_form.cleaned_data['new_password']
        user.set_password(new_password)
        user.save()
        auth.logout(request)

        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
        change_password_form = ChangePasswordForm(request.POST, user=request.user)
        data['msg'] = change_password_form.errors

    return JsonResponse(data)


def forgot_password(request):
    forgot_password_form = ForgotPasswordForm(request.POST, request=request)
    data = {}
    if forgot_password_form.is_valid():
        email = forgot_password_form.cleaned_data['email']
        new_password = forgot_password_form.cleaned_data['new_password']
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        # 清除session
        del request.session['forgot_password_code']

        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'

    return JsonResponse(data)

def send_verification_code(request):
    email = request.GET.get('email')
    send_for = request.GET.get('send_for', '')
    data = {}
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))

        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now

            # 发送邮件
            send_mail(
                '绑定邮箱',
                '验证码: %s' % code,
                '1798615837@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'

    return JsonResponse(data)






