from django.test import TestCase
from LEHU.models import User,Activity,Participant,Message
from LEHU.views import loginForm,registerForm
import json
from django.contrib.auth.hashers import make_password, check_password
import datetime
from django.test.client import Client



class PostTest(TestCase):
    def setUp(self):

        test_data = {'username':'827983519','password': 'a827983519' }

        User.objects.create(user_username = '827983519',
                           user_password = make_password('a827983519'),
                           user_email = '827983519@qq.com',
                           user_gender = 'Male',)

        Message.objects.create(From='827983519a',To='827983519',
                                Content='has joint the event',
                                Title = 'hah',
                                Catagory=2,Activity_id=1,
                                Have_read=0)


        self.client = Client()
        self.client.post('/login',data=test_data)

    def test_post_login(self):
        response = self.client.get('/post')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('post.html')
        self.assertContains(response,'message+icon+new.svg')
        self.assertContains(response,'Activity Title')
        self.assertContains(response,'Catogory')
        self.assertContains(response,'Activity contents')
        self.assertContains(response,'Number of People')
        self.assertContains(response,'Time')
        self.assertContains(response,'Budget')
        self.assertContains(response,'Location')

    def test_post_activity_info_incomplete_login(self):
        test_data = {'title' :'happy','people' : 10,
                    'budget' :12,
                    'time':  datetime.datetime(2019,5,20,12,30,0),
                    'location' : 'Waterloo',
                    'content': "Happy day",
                    'category' : 1}

        response = self.client.post('/post',data=test_data)
        result = json.loads(response.content)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('post.html')
        self.assertEqual(result['user'],'fail')
        self.assertEqual(result['msg'],'Please fill in all information correctly')


    def test_post_activity_info_wrong_login(self):
        test_data = {'title' :'happy','people' : 'assd',
                    'budget' :'ooo',
                    'time':  datetime.datetime(2019,5,20,12,30,0),
                    'location' : 'Waterloo',
                    'content': "Happy day",
                    'category' : 1}

        response = self.client.post('/post',data=test_data)
        result = json.loads(response.content)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('post.html')
        self.assertEqual(result['user'],'fail')
        self.assertEqual(result['msg'],'Please fill in all information correctly')


    def test_post_activity_correct_login(self):
        test_data = {'title' :'happy','people':11,
                    'budget' :12,
                    'time':  datetime.datetime(2019,5,20,12,30,0).strftime('%Y-%m-%dT%H:%M'),
                    'location' : 'Waterloo',
                    'content': "Happy day",
                    'category' :1}

        response = self.client.post('/post',data=test_data)

        activity = Activity.objects.all()

        result = json.loads(response.content)
        self.assertEqual(result['user'],'correct')
        self.assertEqual(activity[0].owner,'827983519')
        self.assertEqual(activity[0].numberofmem,11)
        self.assertEqual(activity[0].budget,12)
        self.assertEqual(activity[0].activity_title,'happy')
        self.assertEqual(activity[0].location,'Waterloo')
        self.assertEqual(activity[0].activity_content,'Happy day')
        self.assertEqual(activity[0].Category,1)
        self.assertEqual(activity[0].start_date, datetime.date(2019,5,20))
        self.assertEqual(activity[0].start_time,datetime.time(12,30,0))
