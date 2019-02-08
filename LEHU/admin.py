from django.contrib import admin

# Register your models here.
from .models import User

class UserAdmin(admin.ModelAdmin):

    list_display = ['user_username','user_gender','user_createTime']
    list_filter = ['user_gender','user_createTime']

    search_fields = ['user_gender','user_createTime']
    list_per_page = 10


admin.site.register(User,UserAdmin)
