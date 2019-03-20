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
    url('^activity',views.activity),
    url('^history',views.history),
    url('^message',views.unread_message),
    url('^allmessage',views.all_message),
    url('^pdetail/(\w+)',views.view_other_profile),
    url('^refresh',views.refresh_recommend),
    #path()

]
