from . import views
from django.urls import path,re_path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url('^$',views.main,name='main'),
    url('^login',views.login,name='login'),
    #url('^logout',views.logout,name='logout'),
    url('^register',views.register,name='register'),
    url('^upload',views.upload),
    url('^profile',views.modify_profile),
    url('^logout',views.logout),
    #path()

]
