from . import views
from django.urls import path,re_path
from django.conf.urls import url



urlpatterns = [
    path('',views.index),

]
