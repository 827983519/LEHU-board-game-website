from django.contrib import admin

# Register your models here.
from .models import User,Activity,Participant,Message,Store


class UserAdmin(admin.ModelAdmin):

    list_display = ['user_username','user_gender','user_createTime','user_image']
    list_filter = ['user_gender','user_createTime']

    search_fields = ['user_gender','user_createTime']
    list_per_page = 10

class ActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_id','activity_title','owner','numberofmem','status']


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['activity_id','participant']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['Activity_id','From','To','Content','CreateTime']


class StoreAdmin(admin.ModelAdmin):
    list_display = ['Store_name','Website','Picture','Popular_board_game1','Popular_board_game2','Popular_board_game3',
    'Location','Location','Rating']


admin.site.register(User,UserAdmin)
admin.site.register(Activity,ActivityAdmin)
admin.site.register(Participant,ParticipantAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Store,StoreAdmin)
