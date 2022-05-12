from .forms import LoginForm, ForgotPasswordForm, RemindMessageFORM
from reply_card.models import MessageNum
from django.contrib.auth.models import User, AnonymousUser
from blog.models import Blog
from django.shortcuts import render ,HttpResponse,redirect



def login_modal_form(request):
    return {'login_modal_form': LoginForm()}

def forgot_password_form(request):
    return {'forgot_password_form': ForgotPasswordForm()}

def remind_message(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            return {'remind_message': MessageNum.objects.get(user=user)}
        except MessageNum.DoesNotExist:
            message_num = MessageNum()
            message_num.num = 0
            message_num.user = user
            message_num.save()
    else:
        return ''

