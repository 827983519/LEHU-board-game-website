from django.test import TestCase
from LEHU.models import User,Activity,Participant,Message
from LEHU.views import loginForm,registerForm
import json
from django.contrib.auth.hashers import make_password, check_password
import datetime
from django.test.client import Client


class ActivityTest(TestCase):
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

    def test_activity_login(self):
        response = self.client.get('/activity')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('activities.html')
        self.assertContains(response,'message+icon+new.svg')

    def test_activity_no_activity(self):
        response = self.client.get('/activity')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('activities.html')
        self.assertContains(response,'[Activities not attended]')
        self.assertContains(response,'[No host activity]')

    def test_activity_1host_activity(self):
        Activity.objects.create(owner = '827983519',numberofmem = 10,
                                    activity_title = 'happy', budget =12,
                                    start_date =  datetime.date(2019,5,20),
                                    start_time = datetime.time(12,30,0),
                                    location = 'Waterloo',
                                    activity_content = "Happy day",
                                    Category = 1, status=1)


        response = self.client.get('/activity')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('activities.html')
        self.assertContains(response,'[Activities not attended]')
        self.assertContains(response,'[happy]')
        self.assertContains(response,'Open')
        self.assertContains(response, datetime.date(2019,5,20).strftime('%B %d, %Y'))
        self.assertContains(response, datetime.time(12,30,0).strftime('%H:%M'))



    def test_activity_2register_activity(self):
        Activity.objects.create(owner = '827983519a',numberofmem = 10,
                                    activity_title = 'happy', budget =12,
                                    start_date =  datetime.date(2019,5,20),
                                    start_time = datetime.time(12,30,0),
                                    location = 'Waterloo',
                                    activity_content = "Happy day",
                                    Category = 1, status=1,activity_id = 1)

        Activity.objects.create(owner = '827983519a',numberofmem = 10,
                                    activity_title = 'sad', budget =12,
                                    start_date =  datetime.date(2019,7,22),
                                    start_time = datetime.time(12,31,0),
                                    location = 'Toronto',
                                    activity_content = "Sad day",
                                    Category = 1, status=1,activity_id = 2)

        activity = Activity.objects.all()
        Participant.objects.create(activity_id = activity[0],participant='827983519')
        Participant.objects.create(activity_id = activity[1],participant='827983519')

        response = self.client.get('/activity')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('activities.html')
        self.assertContains(response,'[No host activity]')
        self.assertContains(response,'[happy]')
        self.assertContains(response,'Open')
        self.assertContains(response, datetime.date(2019,5,20).strftime('%B %d, %Y'))
        self.assertContains(response, datetime.time(12,30,0).strftime('%H:%M'))

        self.assertContains(response,'[sad]')
        self.assertContains(response,'Open')
        self.assertContains(response, datetime.date(2019,7,22).strftime('%B %d, %Y'))
        self.assertContains(response, datetime.time(12,31,0).strftime('%H:%M'))


class HistoryTest(TestCase):
    def setUp(self):

        test_data = {'username':'827983519','password': 'a827983519' }

        User.objects.create(user_username = '827983519',
                           user_password = make_password('a827983519'),
                           user_email = '827983519@qq.com',
                           user_gender = 'Male',)

        self.client = Client()
        self.client.post('/login',data=test_data)

    def test_activity_no_open_activity(self):
        Activity.objects.create(owner = '827983519',numberofmem = 10,
                                    activity_title = 'happy', budget =12,
                                    start_date =  datetime.date(2019,5,20),
                                    start_time = datetime.time(12,30,0),
                                    location = 'Waterloo',
                                    activity_content = "Happy day",
                                    Category = 1, status=1)

        Activity.objects.create(owner = '827983519a',numberofmem = 10,
                                    activity_title = 'sad', budget =12,
                                    start_date =  datetime.date(2019,7,22),
                                    start_time = datetime.time(12,31,0),
                                    location = 'Toronto',
                                    activity_content = "Sad day",
                                    Category = 1, status=1)

        response = self.client.get('/history')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('history.html')
        self.assertContains(response,'[Activities not attended]')
        self.assertContains(response,'[No host activity]')

    def test_activity_host_register_activity(self):
        Activity.objects.create(owner = '827983519',numberofmem = 10,
                                    activity_title = 'happy', budget =12,
                                    start_date =  datetime.date(2019,5,20),
                                    start_time = datetime.time(12,30,0),
                                    location = 'Waterloo',
                                    activity_content = "Happy day",
                                    Category = 1, status=2,activity_id = 1)

        Activity.objects.create(owner = '827983519a',numberofmem = 10,
                                    activity_title = 'sad', budget =12,
                                    start_date =  datetime.date(2019,7,22),
                                    start_time = datetime.time(12,31,0),
                                    location = 'Toronto',
                                    activity_content = "Sad day",
                                    Category = 1, status=2,activity_id = 2)

        activity = Activity.objects.all()
        # print(activity[1].owner)
        Participant.objects.create(activity_id = activity[1],participant='827983519')

        response = self.client.get('/history')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('history.html')
        self.assertContains(response,'[happy]')
        self.assertContains(response,'Closed')
        self.assertContains(response, datetime.date(2019,5,20).strftime('%B %d, %Y'))
        self.assertContains(response, datetime.time(12,30,0).strftime('%H:%M'))

        self.assertContains(response,'[sad]')
        self.assertContains(response,'Closed')
        self.assertContains(response, datetime.date(2019,7,22).strftime('%B %d, %Y'))
        self.assertContains(response, datetime.time(12,31,0).strftime('%H:%M'))
