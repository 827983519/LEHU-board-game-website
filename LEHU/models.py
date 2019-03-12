from django.db import models
from django.utils import timezone

'''
null
如果为True，Django将在数据库中存储一个空值NULL。默认为 False。
blank
如果为True，则允许该字段为空白。默认为False。
注意，该项与null是不同的，null纯粹是与数据库相关的。而blank则与验证相关。如果一个字段设置为blank=True，表单验证时允许输入一个空值。而blank=False，则该项必需输入数据。
'''

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

    def __str__(self):
        return str(self.user_username)


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
    pub_date = models.DateTimeField(auto_now_add=True)
    now = timezone.now()
    start_date = models.DateField('start date')
    start_time = models.TimeField('start time', null = True,blank=True)
    location = models.TextField(null = True, blank = True)
    def publish(self):
        self.pub_date = timezone.now()
        self.save()
    def __str__(self):
        return self.activity_title



class Participant(models.Model):
    activity_id = models.ForeignKey('Activity',on_delete=models.CASCADE)
    participant = models.CharField(max_length=20)

    def __str__(self):
        return self.participant


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

    Activity_id = models.ForeignKey('Activity',on_delete=models.CASCADE)
    Have_read =  models.IntegerField(choices=READ_CHOICES, default=0)
    CreateTime = models.DateTimeField(verbose_name='CreatTime',auto_now_add=True)
    def __str__(self):
        return str(self.From)
