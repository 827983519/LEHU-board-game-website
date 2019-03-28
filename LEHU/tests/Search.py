from django.test import TestCase
from LEHU.models import User,Activity,Participant,Message
from LEHU.views import loginForm,registerForm
import json
from django.contrib.auth.hashers import make_password, check_password
import datetime
from django.test.client import Client



class SearchTest(TestCase):
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

    def test_search_login(self):
        response = self.client.get('/search',data={'q':1})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('search.html')
        self.assertContains(response,'message+icon+new.svg')

    def test_search_no_activity(self):
        response = self.client.get('/search',data={'q':1})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('search.html')
        self.assertContains(response,'No activities matched your search criteria.')

    def test_search_match_activity(self):

        Activity.objects.create(owner = '827983519a',numberofmem = 10,
                                        activity_title = 'happy', budget =12,
                                        start_date =  datetime.date(2019,5,20),
                                        start_time = datetime.time(12,30,0),
                                        location = 'Waterloo',
                                        activity_content = "Happy day",
                                        Category = 1, status=1)

        Activity.objects.create(owner = '827983519a',numberofmem = 10,
                                        activity_title = 'happy1', budget =12,
                                        start_date =  datetime.date(2019,6,20),
                                        start_time = datetime.time(12,31,0),
                                        location = 'Toronto',
                                        activity_content = "Happy1 day",
                                        Category = 1, status=3)
        response = self.client.get('/search',data={'q':'happy'})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('search.html')
        self.assertContains(response,'[happy]')
        self.assertContains(response,'Open')
        self.assertContains(response, datetime.date(2019,5,20).strftime('%B %d, %Y'))
        self.assertContains(response, datetime.time(12,30,0).strftime('%H:%M'))

        self.assertContains(response,'[happy1]')
        self.assertContains(response,'Full')
        self.assertContains(response, datetime.date(2019,6,20).strftime('%B %d, %Y'))
        self.assertContains(response, datetime.time(12,31,0).strftime('%H:%M'))
