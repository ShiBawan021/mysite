from django.urls import path
from . import views

urlpatterns = [
    path('collect_change', views.collect_change, name='collect_change'),
]