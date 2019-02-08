from . import views
from django.urls import path,re_path
from django.conf.urls import url



urlpatterns = [
    #url('^$',views.main,name='main'),
    #url('^login',views.login,name='login'),
    #url('^logout',views.logout,name='logout'),
    #url('^register',views.register,name='register'),
    url('^upload',views.upload),
    #url(r'^login/',)

]
