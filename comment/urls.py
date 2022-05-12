from django.urls import path
from . import views

urlpatterns = [
    path('updata_comment', views.updata_comment, name='Update_Comment')
]