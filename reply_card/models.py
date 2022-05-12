from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.

class ReplyCard(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    comment_type = models.CharField(max_length=15, null=True)
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='reply_card', on_delete=models.DO_NOTHING)
    comment_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    url = models.CharField(max_length=15, null=True)

class MessageNum(models.Model):
    num = models.IntegerField(default=0)
    user = models.ForeignKey(User, related_name='message_num', on_delete=models.DO_NOTHING)