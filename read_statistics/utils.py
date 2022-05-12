import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadDetail

def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key="%s_%s_read"%(ct.model,obj.pk)
    if not request.COOKIES.get(key):
        #旧阅读记数
        # if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
        #     readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        # else:
        #     readnum = ReadNum(content_type=ct, object_id=obj.pk)

        # 新阅读记数 obj,created =get_or_creat
        readnum,created=ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)

        readnum.read_num += 1
        readnum.save()

        date = timezone.now().date()
        # 旧阅读记数
        # if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk,date=date).count():
        #     readDetail=ReadDetail.objects.get(content_type=ct,object_id=obj.pk,date=date)
        # else:
        #     readDetail = ReadDetail(content_type=ct, object_id=obj.pk, date=date)

        # 新阅读记数 obj,created =get_or_creat
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)

        readDetail.read_num+=1
        readDetail.save()
    return key

def get_seven_days_read_data(content_type):
    today=timezone.now().date()
    read_nums=[]
    dates=[]
    for i in range(6,-1,-1):
        date=today - datetime.timedelta(days=i)
        read_detail=ReadDetail.objects.filter(content_type=content_type, date=date)
        result=read_detail.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
        dates.append(date.strftime('%m/%d'))
        # print(result['read_num_sum'])
        # print(today)
        # print(date)
    return dates,read_nums

def get_today_hot_data(content_type):
    today=timezone.now().date()
    read_detail=ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-read_num')
    return read_detail[:7]

def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_detail = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_detail[:7]

def get_7_days_hot_data(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    read_detail=ReadDetail.objects\
                          .filler(content_type=content_type, date__lt = today, date__gte =date ) \
                          .annotate(read_num_sum=Sum('read_num'))\
                          .oredr_by('-read_num_sum')
    return read_detail[:7]

def get_orther_blog():
    read_detail = ReadNum.objects.order_by('-read_num')
    return read_detail[:7]