# Create your models here.
import datetime

from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    activity_title = models.CharField(max_length=200)
    activity_content = models.TextField(null=True, blank =True)

    # STATUS_CHOICES = (
    #     (1, 'Open'),
    #     (2, 'Closed'),
    #     (3, 'On-going'),
    #     (4, 'Cancel'),
    #     (5, 'Pending'),
    # )
    # status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    owner = models.CharField(max_length=200, null=True, blank =True)
    numberofmem = models.PositiveSmallIntegerField('Number of People', null=True, blank =True)
    budget = models.PositiveSmallIntegerField(null=True, blank =True)
    # pub_date = models.DateTimeField(auto_now_add=True, 'date published')
    pub_date = models.DateTimeField(auto_now_add=True)
    now = timezone.now()
    start_time = models.DateTimeField('start time', default=now,blank=True)
    duration = models.TimeField('duration', null = True)
    location = models.TextField(null = True, blank = True)
    def publish(self):
        self.pub_date = timezone.now()
        self.save()
    def __str__(self):
        return self.activity_title
    # def was_published_recently(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(days = 1) <= self.pub_date <= now

class ActivityForm(ModelForm):
    #  def __init__(self, *args, **kwargs): 
    #     super(ModelForm, self).__init__(*args, **kwargs)
    #     self.css_class = "rule"
    #  def __init__(self, *args, **kwargs):
    #     super(MyForm, self).__init__(*args, **kwargs)
    #     self.fields['Activity'].widget.attrs.update({'class' : 'fields'})
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['activity_title'].widget.attrs.update({'class': 'fields'})
        self.fields['activity_title'].widget.attrs.update(size='40')
    
    class Meta:
        model = Activity
        now = timezone.now()
        fields = []
        labels = {
            'numberofmem': _('Number of people'),
        }
        #start_time = forms.DateTimeField(initial=now, required=False)

# '''
# null
# 如果为True，Django将在数据库中存储一个空值NULL。默认为 False。
# blank
# 如果为True，则允许该字段为空白。默认为False。
# 注意，该项与null是不同的，null纯粹是与数据库相关的。而blank则与验证相关。如果一个字段设置为blank=True，表单验证时允许输入一个空值。而blank=False，则该项必需输入数据。
# '''

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user/{0}/{1}'.format(instance.username, filename)


class Picture(models.Model):
    Image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    username = models.CharField(verbose_name='Username',max_length = 20,null=True,blank=True)

def profile_picture_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user/{0}/{1}'.format(instance.user_username, filename)

class User(models.Model):
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
    )
    #user_id = models.IntegerField(verbose_name='ID',primary_key=True)
    user_username = models.CharField(verbose_name='Username',primary_key=True,max_length = 20)
    user_nickname = models.CharField(verbose_name='Nickname',max_length = 20,null=True,blank=True)
    user_password = models.CharField(verbose_name='Password',max_length = 100)
    user_gender = models.CharField(verbose_name='Gender',max_length=10,  choices=(("Female", u'Female'), ("Male", u'Male')), default='Male')
    user_createTime = models.DateField(verbose_name='CreatTime',auto_now_add=True)
    user_email = models.CharField(verbose_name='Email',max_length = 20,null=True,blank=True)
    user_province = models.CharField(verbose_name='Province',max_length = 20,null=True,blank=True)
    user_city = models.CharField(verbose_name='City',max_length = 20,null=True,blank=True)
    user_bio = models.CharField(verbose_name='Bio',max_length=100,null=True,blank=True)
    user_favouritegame = models.CharField(verbose_name='Favourite game',max_length=50,null=True,blank=True)
    user_cellphone = models.CharField(verbose_name='Cell phone',max_length = 15,null=True,blank=True)
    user_image = models.ImageField(upload_to=profile_picture_path, blank=True, null=True)


    '''
    user_image = models.ImageField(upload_to=u'image/%Y/%m', default=u"image/default.png", max_length=100,null=True, blank=True)
    '''

    def __str__(self):
        return str(self.user_username)
