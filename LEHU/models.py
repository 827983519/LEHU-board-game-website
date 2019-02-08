from django.db import models


'''
null
如果为True，Django将在数据库中存储一个空值NULL。默认为 False。
blank
如果为True，则允许该字段为空白。默认为False。
注意，该项与null是不同的，null纯粹是与数据库相关的。而blank则与验证相关。如果一个字段设置为blank=True，表单验证时允许输入一个空值。而blank=False，则该项必需输入数据。
'''

class Picture(models.Model):
    Image = models.ImageField(upload_to='user/', blank=True, null=True)
    def __str__(self):
        return self.Image

class User(models.Model):
    GENDER_CHOICES = (
        (u'M', u'Male'),
        (u'F', u'Female'),
    )
    #user_id = models.IntegerField(verbose_name='ID',primary_key=True)
    user_username = models.CharField(verbose_name='Username',primary_key=True,max_length = 20)
    user_password = models.CharField(verbose_name='Password',max_length = 50)
    user_gender = models.CharField(verbose_name='Gender',max_length=10,  choices=(("Female", u'Female'), ("Male", u'Male')), default='Male')
    user_createTime = models.DateField(verbose_name='CreatTime',auto_now_add=True)
    user_email = models.CharField(verbose_name='Email',max_length = 20,null=True,blank=True)
    user_province = models.CharField(verbose_name='Province',max_length = 20,null=True,blank=True)
    user_city = models.CharField(verbose_name='City',max_length = 20,null=True,blank=True)
    user_bio = models.CharField(verbose_name='Bio',max_length=100,null=True,blank=True)
    user_favouritegame = models.CharField(verbose_name='Favourite game',max_length=50,null=True,blank=True)
    user_cellphone = models.CharField(verbose_name='Cell phone',max_length = 15,null=True,blank=True)
    user_image = models.ImageField(upload_to='user', blank=True, null=True)

    '''
    user_image = models.ImageField(upload_to=u'image/%Y/%m', default=u"image/default.png", max_length=100,null=True, blank=True)
    '''

    def __str__(self):
        return str(self.user_username)
