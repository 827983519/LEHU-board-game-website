from django.test import TestCase
from LEHU.models import User,Activity,Participant,Message
from LEHU.views import loginForm,registerForm
import json
from django.contrib.auth.hashers import make_password, check_password
import datetime
from django.test.client import Client


class MessageTest(TestCase):
    def setUp(self):

        test_data = {'username':'827983519','password': 'a827983519' }

        User.objects.create(user_username = '827983519',
                           user_password = make_password('a827983519'),
                           user_email = '827983519@qq.com',
                           user_gender = 'Male',)

        Activity.objects.create(owner = '827983519',numberofmem = 10,
                                    activity_title = 'happy', budget =12,
                                    start_date =  datetime.date(2019,5,20),
                                    start_time = datetime.time(12,30,0),
                                    location = 'Waterloo',
                                    activity_content = "Happy day",
                                    Category = 1, status=1)
        self.client = Client()
        self.client.post('/login',data=test_data)

    def test_no_unread_message_login(self):
        response = self.client.get('/message')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('Unread.html')
        self.assertContains(response,'[No new message]')

    def test_no_allmessage_login(self):
        response = self.client.get('/allmessage')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('Read.html')
        self.assertContains(response,'[No message]')

    def test_1unread_message(self):
        activity = Activity.objects.all()
        Message.objects.create(From='827983519a',To='827983519',
                                Content='has joint the event',
                                Title = activity[0].activity_title,
                                Catagory=2,Activity_id=activity[0].activity_id,
                                Have_read=0)

        response = self.client.get('/message')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('Unread.html')
        self.assertContains(response,'[happy]')
        self.assertContains(response,'827983519a</a> has joint the event')

    def test_2unread_message(self):
        activity = Activity.objects.all()
        Message.objects.create(From='827983519a',To='827983519',
                                Content='has joint the event',
                                Title = activity[0].activity_title,
                                Catagory=2,Activity_id=activity[0].activity_id,
                                Have_read=0)

        Message.objects.create(From='827983519a',To='827983519',
                                Content='has quit the event',
                                Title = activity[0].activity_title,
                                Catagory=1,Activity_id=activity[0].activity_id,
                                Have_read=0)

        response = self.client.get('/message')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('Unread.html')
        self.assertContains(response,'[happy]')
        self.assertContains(response,'827983519a</a> has joint the event')

        self.assertTemplateUsed('Unread.html')
        self.assertContains(response,'[happy]')
        self.assertContains(response,'827983519a</a> has quit the event')

    def test_1read_message(self):
        activity = Activity.objects.all()
        Message.objects.create(From='827983519a',To='827983519',
                                Content='has joint the event',
                                Title = activity[0].activity_title,
                                Catagory=2,Activity_id=activity[0].activity_id,
                                Have_read=1)

        response = self.client.get('/allmessage')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('Read.html')
        self.assertContains(response,'[happy]')
        self.assertContains(response,'827983519a</a> has joint the event')

    def test_2all_message(self):
        activity = Activity.objects.all()
        Message.objects.create(From='827983519a',To='827983519',
                                Content='has joint the event',
                                Title = activity[0].activity_title,
                                Catagory=2,Activity_id=activity[0].activity_id,
                                Have_read=1)

        Message.objects.create(From='827983519a',To='827983519',
                                Content='has quit the event',
                                Title = activity[0].activity_title,
                                Catagory=1,Activity_id=activity[0].activity_id,
                                Have_read=1)

        response = self.client.get('/allmessage')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('Read.html')
        self.assertContains(response,'[happy]')
        self.assertContains(response,'827983519a</a> has joint the event')

        self.assertTemplateUsed('Unread.html')
        self.assertContains(response,'[happy]')
        self.assertContains(response,'827983519a</a> has quit the event')
