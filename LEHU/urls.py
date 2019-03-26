from . import views
from django.urls import path,re_path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url('^$',views.main,name='main'),
    url('^login',views.login,name='login'),
    url('^register',views.register,name='register'),
    url('^profile',views.modify_profile),
    url('^logout',views.logout),
    url('^search',views.search),
    url('^activity',views.activity),
    url('^history',views.history),
    url('^message',views.unread_message),
    url('^allmessage',views.all_message),
    url('^pdetail/(\w+)',views.view_other_profile),
    url('^refresh',views.refresh_recommend),
    url('^post', views.ActivityPostView.as_view(), name='activitypost'),
    # url('^index', views.PostListView.as_view(), name = 'postlist'),
    path('details/<int:pk>/', views.PostDetailView.as_view(), name = 'detail'),
    path('details/<int:activity_id>/join', views.join, name='join'),
    path('details/<int:pk>/update', views.ActivityUpdateView.as_view(), name = 'update'),
    path('details/<int:activity_id>/cancel', views.cancel, name='cancel'),
    path('details/<int:activity_id>/quit', views.quit, name='quit'),
    path('join_fail', views.JoinFailedView.as_view(), name='join_fail'),
    url('^$',views.main,name='main'),
]
