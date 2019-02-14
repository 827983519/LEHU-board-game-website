from . import views
from django.urls import path,re_path
from django.conf.urls import url



urlpatterns = [
    path('',views.IndexView.as_view, name = 'index'),
    path('post/new/', views.ActivityPostView.as_view(), name='activitypost'),
    #url('^post/new/', views.ActivityPostView.as_view(), name='activitypost'),
    path('post/list/', views.PostListView.as_view(), name = 'postlist'),
    #url('^post/list/', views.PostListView.as_view(), name = 'postlist'),
    path('post/details/<slug:pk>/', views.PostDetailView.as_view(), name = 'detail'),
    #url('^post/details/<slug:pk>/', views.PostDetailView.as_view(), name = 'detail'),

]