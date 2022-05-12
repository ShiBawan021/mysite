from django.contrib import admin
from .models import CollectCount, CollectRecord
# Register your models here.

@admin.register(CollectCount)
class CollectNumAdmin(admin.ModelAdmin):
    list_display = ('id', 'collect_num')

@admin.register(CollectRecord)
class CollectRecord(admin.ModelAdmin):
    list_display = ('id', 'collect_time')