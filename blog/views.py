from django.shortcuts import get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.shortcuts import render, redirect
from read_statistics.utils import read_statistics_once_read, get_orther_blog
from .forms import EditForm, ContributionForm



# Create your views here.



def get_blog_list_common_data(request,blogs_all_list):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOG_NUMBER)
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

    #统计各类博客的博客数量
    # blog_types=BlogType.objects.all()
    # blog_types_list=[]
    # for blog_type in blog_types:
    #     blog_type.blog_type_count=Blog.objects.filter(blog_type=blog_type).count()
    #     blog_types_list.append(blog_type)
    #     print(blog_types_list)

    #统计日期归档各日期博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_dates_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_dates_count

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()

    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request,blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)
    # 其他博客
    orther_blog = get_orther_blog()

    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['next_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['blog'] = blog
    context['orther_blog'] = orther_blog


    response=render(request,'blog/blog_detail.html',context)#响应
    response.set_cookie(read_cookie_key,'true')#阅读标记

    return response

def blogs_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)

def blogs_with_dates(request,year,month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blogs_with_dates.html', context)

def edit_blog(request):
    blog_id = request.GET.get('from', '')
    blog = Blog.objects.get(id=blog_id)
    blog_time = blog.created_time
    context = {}
    if request.user == blog.author:
        context['blog'] = blog
        if request.method == 'POST':
            edit_form = EditForm(request.POST, user=request.user)
            if edit_form.is_valid():
                blog = Blog()
                # blog_type = BlogType.objects.all()[0]
                # 获取博客类型blog_type
                blog_type_id = int(edit_form.cleaned_data['blog_type'])
                blog_type = BlogType.objects.all()[blog_type_id-1]
                title = edit_form.cleaned_data['title']
                text = edit_form.cleaned_data['text']
                user = request.user
                blog.blog_type = blog_type
                blog.title = title
                blog.content = text
                blog.author = user
                blog.created_time = blog_time
                blog._set_pk_val(blog_id)
                blog.save()
                edited_blog = Blog.objects.get(id=blog_id)
                reverse_to = "http://localhost:8000/blog/"+str(edited_blog.id)
                return redirect(reverse_to)
        else:
            edit_form = EditForm()


    context['edit_form'] = edit_form

    return render(request, 'user/edit.html', context)

def contribution(request):
    if request.method == 'POST':
        contribution_form = ContributionForm(request.POST, user=request.user)
        if contribution_form.is_valid():
            blog = Blog()
            # blog_type = BlogType.objects.all()[0]
            # 获取博客类型blog_type
            blog_type_id = int(contribution_form.cleaned_data['blog_type'])
            blog_type = BlogType.objects.all()[blog_type_id-1]
            title = contribution_form.cleaned_data['title']
            text = contribution_form.cleaned_data['text']
            user = request.user
            blog.blog_type = blog_type
            blog.title = title
            blog.content = text
            blog.author = user
            blog.save()
            new_blog = Blog.objects.all().first()
            reverse_to = "http://localhost:8000/blog/" + str(new_blog.id)
            return redirect(reverse_to)
    else:
        contribution_form = ContributionForm()

    context = {}
    context['contribution_form'] = contribution_form
    return render(request, 'user/contribution.html', context)