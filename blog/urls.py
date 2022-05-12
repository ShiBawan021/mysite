from django.urls import path
from . import views

#start with blog
urlpatterns = [
    #http:/localhost:8000/1
    path('',views.blog_list,name='Blog_list'),
    path("<int:blog_pk>", views.blog_detail, name="Blog_detail"),
    path('type/<int:blog_type_pk>',views.blogs_with_type,name="Blogs_with_type"),
    path('date/<int:year>/<int:month>',views.blogs_with_dates,name="Blogs_with_dates"),
    path('edit_blog', views.edit_blog, name='edit_blog'),
    path('contribution/', views.contribution, name='contribution'),
]