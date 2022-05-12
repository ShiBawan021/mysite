from django.contrib import admin
from .models import ReplyCard, MessageNum

# Register your models here.

@admin.register(ReplyCard)
class ReplyCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'comment_time', 'comment_type')

@admin.register(MessageNum)
class ReplyCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'num')