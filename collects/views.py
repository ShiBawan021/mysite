from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import CollectCount, CollectRecord


def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def SuccessResponse(collect_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['collect_num'] = collect_num
    return JsonResponse(data)

def collect_change(request):
    # 获取数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, 'you were not login')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, 'object not exist')

    # 处理数据
    if request.GET.get('is_collect') == 'true':
        # 要点赞
        collect_record, created = CollectRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 未点赞过，进行点赞
            collect_count, created = CollectCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            collect_count.collect_num += 1
            collect_count.save()
            return SuccessResponse(collect_count.collect_num)
        else:
            # 已点赞过，不能重复点赞
            return ErrorResponse(402, 'you were collect')
    else:
        # 要取消点赞
        if CollectRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有点赞过，取消点赞
            collect_record = CollectRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            collect_record.delete()
            # 点赞总数减1
            collect_count, created = CollectCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                collect_count.collect_num -= 1
                collect_count.save()
                return SuccessResponse(collect_count.collect_num)
            else:
                return ErrorResponse(404, 'data error')
        else:
            # 没有点赞过，不能取消
            return ErrorResponse(403, 'you were not collect')