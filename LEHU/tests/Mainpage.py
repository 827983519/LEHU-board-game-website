from django.test import TestCase
from LEHU.models import User,Activity,Participant,Store,Message
from LEHU.views import loginForm,registerForm
import json
from django.contrib.auth.hashers import make_password, check_password
import datetime
from django.test.client import Client



class MainpageTest(TestCase):
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
        Store.objects.create(Store_name='Store1',Location='Waterloo',Picture='store/1.jpeg',Rating=4)
        Store.objects.create(Store_name='Store2',Location='Waterloo',Picture='store/2jpeg',Rating=4.1)
        Store.objects.create(Store_name='Store3',Location='Toronto',Picture='store/3.jpeg',Rating=4.3)
        Store.objects.create(Store_name='Store4',Location='Toronto',Picture='store/4.jpeg',Rating=4.5)
        Store.objects.create(Store_name='Store5',Location='Waterloo',Picture='store/5.jpeg',Rating=4.2)
        Store.objects.create(Store_name='Store6',Location='Toronto',Picture='store/6.jpeg',Rating=3.9)

        self.client = Client()
        self.client.post('/login',data=test_data)

    def test_main_page_no_activity_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('index_new.html')
        self.assertContains(response,'Waterloo')
        self.assertContains(response,'Toronto')
        self.assertContains(response,'.jpeg')
        self.assertContains(response,'message+icon+new.svg')
        

    def test_main_page_activity_login(self):
        Activity.objects.create(owner = '827983519a',numberofmem = 10,
                                    activity_title = 'happy', budget =12,
                                    start_date =  datetime.date(2019,5,20),
                                    start_time = datetime.time(12,30,0),
                                    location = 'Paris',
                                    activity_content = "Happy day",
                                    Category = 1, status=1)

        Activity.objects.create(owner = '827983519a',numberofmem = 10,
                                    activity_title = 'happy1', budget =12,
                                    start_date =  datetime.date(2019,5,20),
                                    start_time = datetime.time(12,30,0),
                                    location = 'Paris',
                                    activity_content = "Happy day",
                                    Category = 1, status=1)

        Activity.objects.create(owner = '827983519a',numberofmem = 10,
                                    activity_title = 'happy2', budget =12,
                                    start_date =  datetime.date(2019,5,20),
                                    start_time = datetime.time(12,30,0),
                                    location = 'Paris',
                                    activity_content = "Happy day",
                                    Category = 1, status=1)
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('index_new.html')
        self.assertContains(response,'Paris')
        self.assertContains(response,'happy')
        self.assertContains(response,'2019')
        self.assertContains(response,'May')
