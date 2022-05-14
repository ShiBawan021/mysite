"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('login_for_modal/', views.login_for_modal, name='login_for_modal'),
    path('register/', views.register, name='register'),
    path('login_form/', views.login_form, name='login_form'),
    path('register_form/', views.register_form, name='register_form'),
    path('logout/', views.logout, name='logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    path('change_email/', views.change_email, name='change_email'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('reply_card_del/', views.reply_card_del, name='reply_card_del'),
    path('', views.reply_card_url, name='reply_card_url'),
    path('blog_del/', views.blog_del, name='blog_del'),
    path('collect_del/', views.collect_del, name='collect_del'),
    path('clear_message_num/', views.clear_message_num, name='clear_message_num'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)