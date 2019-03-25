# Create your models here.
import datetime

from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.db.models import Count

# Create your models here.

class Activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    activity_title = models.CharField(max_length=200)
    activity_content = models.TextField(null=True, blank =True)

    STATUS_CHOICES = (
        (1, 'Open'),
        (2, 'Closed'),
        (3, 'Full'),
        (4, 'Cancel'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    CATEGORY_CHOICES = (
        (1, 'Card'),
        (2, 'Chess'),
        (3, 'BoardGames'),
        (4, 'Others'),
    )
    Category = models.IntegerField(choices=CATEGORY_CHOICES, default=1)

    owner = models.CharField(max_length=200, null=True, blank =True)
    numberofmem = models.PositiveSmallIntegerField('Number of People', null=True, blank =True)
    budget = models.PositiveSmallIntegerField(null=True, blank =True)
    # pub_date = models.DateTimeField(auto_now_add=True, 'date published')
    pub_date = models.DateTimeField(auto_now_add=True)
    now = timezone.now()
    start_date = models.DateField('start date')
    start_time = models.TimeField('start time', null = True,blank=True)
    # duration = models.DurationField('duration', null=True,
    #                                          blank=True,
    #                                          default='00:05:00',
    #                                          help_text=_('[HH:[MM:]]ss[.uuuuuu] format'))
    # duration = models.TimeField('duration', null = True,blank=True)
    location = models.TextField(null = True, blank = True)
    def publish(self):
        self.pub_date = timezone.now()
        self.save()
    def __str__(self):
        return self.activity_id
    # def was_published_recently(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(days = 1) <= self.pub_date <= now

class TimeInput(forms.TimeInput):
    input_type = 'time'
class DateInput(forms.DateInput):
    input_type = 'date'

class ActivityForm(ModelForm):
    #  def __init__(self, *args, **kwargs): 
    #     super(ModelForm, self).__init__(*args, **kwargs)
    #     self.css_class = "rule"
    #  def __init__(self, *args, **kwargs):
    #     super(MyForm, self).__init__(*args, **kwargs)
    #     self.fields['Activity'].widget.attrs.update({'class' : 'fields'})
    def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.fields['activity_title'].widget.attrs.update({'class': 'fields'})
        self.fields['activity_title'].widget.attrs.update(size='40')
    
    class Meta:
        model = Activity
        now = timezone.now()
        fields = ('activity_title','Category','activity_content','numberofmem','start_date','start_time','budget','location')
        # widgets = {
        #     'duration': TimeInput()
        # }

        #start_time = forms.DateTimeField(initial=now, required=False)

class ParticipantManager(models.Manager):
    def create_activity(self, activity_id, participant):
        Participant = self.create(activity_id=activity_id, participant=participant)
        #Participant = self.create(participant=participant)
        # do something with the book
        return Participant
    def member_count(self, activity_id):
        count = self.filter(activity_id=activity_id).count()
        return count
    def find_activity(self, activity_id, participant):
        Participant = self.filter(activity_id=activity_id, participant=participant)
        return Participant
    def get_all_participant(self, activity_id):
        Participant = self.values_list('participant', flat=True).filter(activity_id=activity_id)
        return Participant

    # def create_participant(self, participant):
        
    #     # do something with the book
    #     return Participant

class Participant(models.Model):
    activity_id = models.ForeignKey('Activity',on_delete=models.CASCADE)
    participant = models.CharField(max_length=20)

    objects = ParticipantManager()

    def __str__(self):
        return self.activity_id

 

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

class MessageManager(models.Manager):
    def create_message(self, activity_id, From, To, Content, Catagory):
        #now = timezone.now()
        Message = self.create(Activity_id=activity_id, From=From, To=To, Content=Content, Catagory=Catagory)
        return Message


class Message(models.Model):
    From = models.CharField(max_length = 20)
    To = models.CharField(max_length = 20)
    Content = models.CharField(max_length=50)

    CATEGORY_CHOICES = (
        (1, 'Quit'),
        (2, 'Join'),
        (3, 'Modify'),
        (4, 'Close'),
    )

    Catagory = models.IntegerField(choices=CATEGORY_CHOICES, default=0)
    READ_CHOICES = (
        (1, 'Read'),
        (0, 'Unread'),
    )

    Activity_id = models.IntegerField(null=True, blank =True)
    Have_read =  models.IntegerField(choices=READ_CHOICES, default=0)
    CreateTime = models.DateTimeField(verbose_name='CreatTime',auto_now_add=True)

    objects = MessageManager()

    def __str__(self):
        return str(self.From)
