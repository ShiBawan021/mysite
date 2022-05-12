import threading
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from reply_card.models import ReplyCard, MessageNum
from django.template.loader import render_to_string

class SendMail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=self.fail_silently,
            html_message=self.text,
        )

# Create your models here.

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='comments', on_delete = models.DO_NOTHING)

    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.DO_NOTHING)
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.DO_NOTHING)
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.DO_NOTHING)

    def create_reply_card(self):
        # 发送消息
        reply_card = ReplyCard()
        reply_card.text = self.text
        reply_card.comment_time = self.comment_time
        reply_card.content_type = self.content_type
        reply_card.object_id = self.object_id
        reply_card.url = self.content_object.get_url()
        if self.parent is None:
            reply_card.comment_type = '有新的评论'
            email = self.content_object.get_email()
        else:
            reply_card.comment_type = '有新的回复'
            email = self.reply_to.email

        user = User.objects.get(email=email)
        reply_card.user = user
        reply_card.comment_user = self.user
        reply_card.save()
        message_num = MessageNum.objects.get(user=user)
        message_num.num += 1
        message_num.save()

    # def send_email(self):
    #     # 发送邮件通知
    #     if self.parent is None:
    #         # 评论我的博客
    #         subject = '有新的评论'
    #         email = self.content_object.get_email()
    #     else:
    #         # 回复评论
    #         subject = '有新的回复'
    #         email = self.reply_to.email
    #     if email != '':
    #         context = {}
    #         context['comment_text'] = self.text
    #         context['url'] = self.content_object.get_url()
    #         text = render_to_string('comment/send_mail.html', context)
    #         send_mail = SendMail(subject, text, email)
    #         send_mail.start()

    def __str__(self):
        return self.text


    class Meta:
        ordering = ['-comment_time']



