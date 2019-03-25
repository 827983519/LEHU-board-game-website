from django.contrib import admin
from .models import Activity

# Register your models here.

from .models import User,Picture

class UserAdmin(admin.ModelAdmin):

    list_display = ['user_username','user_gender','user_createTime']
    list_filter = ['user_gender','user_createTime']

    search_fields = ['user_gender','user_createTime']
    list_per_page = 10


class PictureAdmin(admin.ModelAdmin):

    list_display = ['username','Image']


admin.site.register(Activity)
admin.site.register(User,UserAdmin)
admin.site.register(Picture,PictureAdmin)
