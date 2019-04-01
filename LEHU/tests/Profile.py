from django.test import TestCase
from LEHU.models import User,Activity,Participant,Message
from LEHU.views import loginForm,registerForm
import json
from django.contrib.auth.hashers import make_password, check_password
import datetime
from django.test.client import Client



class ProfileTest(TestCase):
    def setUp(self):
        test_data = {'username':'827983519','password': 'a827983519' }

        User.objects.create(user_username = '827983519',
                           user_password = make_password('a827983519'),
                           user_email = '827983519@qq.com',
                           user_gender = 'Male',)

        User.objects.create(user_username = '827983519a',
                           user_password = make_password('a827983519'),
                           user_email = '827983519a@qq.com',
                           user_gender = 'Male',user_nickname='wade',
                          user_bio='I like board game', user_province='Ontario',
                          user_favouritegame='Uno;Three:Hi',user_city='Waterloo',
                          user_cellphone='226978',user_image='picture.jpg')
        Message.objects.create(From='827983519a',To='827983519',
                                Content='has joint the event',
                                Title = 'hah',
                                Catagory=2,Activity_id=1,
                                Have_read=0)
        self.client = Client()
        self.client.post('/login',data=test_data)

    def test_profile_login(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('profile.html')
        self.assertContains(response,'827983519@qq.com')
        self.assertContains(response,'Nickname')
        self.assertContains(response,'Bio')
        self.assertContains(response,'Favourite Board Games')
        self.assertContains(response,'Cellphone Number')
        self.assertContains(response,'Province')
        self.assertContains(response,'City')
        self.assertContains(response,'Email Address')
        self.assertContains(response,'message+icon+new.svg')

    def test_profile_show_info(self):
        test_data1 = {'username':'827983519a','password': 'a827983519' }
        self.client.post('/logout')
        self.client.post('/login',data=test_data1)

        response = self.client.get('/profile')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('profile.html')
        self.assertContains(response,'827983519a@qq.com')
        self.assertContains(response,'wade')
        self.assertContains(response,'I like board game')
        self.assertContains(response,'Three')
        self.assertContains(response,'Hi')
        self.assertContains(response,'Uno')
        self.assertContains(response,'226978')
        self.assertContains(response,'Ontario')
        self.assertContains(response,'Waterloo')

    def test_profile_modify_info(self):
        test_data1 = {'email':'8279835191@qq.com',
                     'nickname':'wade1',
                     'bio':'I like board game1', 'province':'Ontario1',
                     'favourite1':'Uno1','favourite2':'Three1','favourite3':'Hi1',
                     'city':'Waterloo1',
                     'cellphone':'2269781'}

        response = self.client.post('/profile',data = test_data1)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('profile.html')
        self.assertContains(response,'wade1')
        self.assertContains(response,'I like board game1')
        self.assertContains(response,'Three1')
        self.assertContains(response,'Hi1')
        self.assertContains(response,'Uno1')
        self.assertContains(response,'2269781')
        self.assertContains(response,'Ontario1')
        self.assertContains(response,'Waterloo1')

    def test_view_other_profile_info(self):
        response = self.client.post('/pdetail/827983519a')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('profile.html')
        self.assertContains(response,'827983519a@qq.com')
        self.assertContains(response,'wade')
        self.assertContains(response,'I like board game')
        self.assertContains(response,'Three')
        self.assertContains(response,'Hi')
        self.assertContains(response,'Uno')
        self.assertContains(response,'226978')
        self.assertContains(response,'Ontario')
        self.assertContains(response,'Waterloo')
        self.assertContains(response,'picture.jpg')
