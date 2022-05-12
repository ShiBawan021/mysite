from django.contrib import admin
from .models import LikeCount, LikeRecord
# Register your models here.

@admin.register(LikeCount)
class LikedNumAdmin(admin.ModelAdmin):
    list_display = ('id', 'liked_num')

@admin.register(LikeRecord)
class LikeRecord(admin.ModelAdmin):
    list_display = ('id', 'liked_time')