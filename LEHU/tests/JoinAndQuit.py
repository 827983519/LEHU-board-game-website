from django.test import TestCase
from LEHU.models import User,Activity,Participant,Message
from LEHU.views import loginForm,registerForm
import json
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404, render, redirect
import datetime
from django.test.client import Client
from django.urls import reverse,reverse_lazy


class JoinTest(TestCase):

    def test_activity_join_1participant(self):

        self.client = Client()
        #self.client.post('/login',data=test_data)
        test_data1 = {'username':'1111111','password': '1111111' }

        user1 = User.objects.create(user_username = '1111111',
                           user_password = make_password('1111111'),
                           user_email = '827983519@qq.com',
                           user_gender = 'Male',)

        activity1 = Activity.objects.create(owner = '827983519',numberofmem = 2,
                                    activity_title = 'happy', budget =12,
                                    start_date =  datetime.date(2019,5,20),
                                    start_time = datetime.time(12,30,0),
                                    location = 'Waterloo',
                                    activity_content = "Happy day",
                                    Category = 1, status=1)

        self.client.post('/login',data=test_data1)

        #response = self.client.get('/activity')
        response = self.client.get(reverse('join', kwargs={'activity_id': activity1.activity_id}))

        asset = Participant.objects.get(activity_id=activity1.activity_id)

        self.assertEqual(response.status_code,302)
        #self.assertTemplateUsed('event.html')
        self.assertEqual(asset.participant, user1.user_username)
        self.assertEqual(activity1.status, 1)
        # self.assertContains(response,'[Activities not attended]')
        # self.assertContains(response,'[No host activity]')

    def test_activity_join_2participant(self):

        self.client = Client()
        #self.client.post('/login',data=test_data)
        test_data2 = {'username':'2222222','password': '2222222' }
        #test_data1 = {'username':'1111111','password': '1111111' }

        # user1 = User.objects.create(user_username = '1111111',
        #                    user_password = make_password('1111111'),
        #                    user_email = '827983519@qq.com',
        #                    user_gender = 'Male',)

        user2 = User.objects.create(user_username = '2222222',
                           user_password = make_password('2222222'),
                           user_email = '827983519@qq.com',
                           user_gender = 'Female',)

        activity2 = Activity.objects.create(owner = '827983520',numberofmem = 2,
                                    activity_title = 'happy', budget =12,
                                    start_date =  datetime.date(2019,5,20),
                                    start_time = datetime.time(12,30,0),
                                    location = 'Waterloo',
                                    activity_content = "Happy day",
                                    Category = 1, 
                                    status = 1
                                    )

        Participant.objects.create(activity_id = activity2, participant='1111111')
        #Participant.objects.create(activity_id = activity1, participant='3333333')

        self.client.post('/login',data=test_data2)

        #response = self.client.get('/activity')
        response = self.client.get(reverse('join', kwargs={'activity_id': activity2.activity_id}))

        #asset = Participant.objects.filter(activity_id=activity2.activity_id)
        asset = Participant.objects.values_list('participant', flat=True).filter(activity_id=activity2.activity_id)

        activity = get_object_or_404(Activity, pk=activity2.activity_id)
        status = activity.status

        self.assertEqual(response.status_code,302)
        #self.assertTemplateUsed('event.html')
        self.assertQuerysetEqual(list(asset), ["'1111111'", "'2222222'"])
        self.assertEqual(status, 3)


    def test_activity_join_full(self):

        self.client = Client()
        #self.client.post('/login',data=test_data)
        test_data3 = {'username':'3333333','password': '3333333' }
        #test_data1 = {'username':'1111111','password': '1111111' }

        user3 = User.objects.create(user_username = '3333333',
                           user_password = make_password('3333333'),
                           user_email = '827983519@qq.com',
                           user_gender = 'Male',)

        activity3 = Activity.objects.create(owner = '827983520',numberofmem = 2,
                                    activity_title = 'happy', budget =12,
                                    start_date =  datetime.date(2019,5,20),
                                    start_time = datetime.time(12,30,0),
                                    location = 'Waterloo',
                                    activity_content = "Happy day",
                                    Category = 1, 
                                    status = 3
                                    )

        Participant.objects.create(activity_id = activity3, participant='1111111')
        Participant.objects.create(activity_id = activity3, participant='2222222')
        #Participant.objects.create(activity_id = activity1, participant='3333333')

        self.client.post('/login',data=test_data3)

        #response = self.client.get('/activity')
        response = self.client.get(reverse('join', kwargs={'activity_id': activity3.activity_id}))

        #asset = Participant.objects.filter(activity_id=activity2.activity_id)
        asset = Participant.objects.values_list('participant', flat=True).filter(activity_id=activity3.activity_id)

        self.assertEqual(response.status_code,302)
        #self.assertTemplateUsed('event.html')
        self.assertQuerysetEqual(list(asset), ["'1111111'", "'2222222'"])
        self.assertEqual(activity3.status, 3)


class QuitTest(TestCase):
    def test_activity_quit(self):

        self.client = Client()
        #self.client.post('/login',data=test_data)
        test_data2 = {'username':'2222222','password': '2222222' }
        #test_data1 = {'username':'1111111','password': '1111111' }

        user2 = User.objects.create(user_username = '2222222',
                           user_password = make_password('2222222'),
                           user_email = '827983519@qq.com',
                           user_gender = 'Female',)

        activity = Activity.objects.create(owner = '827983520',numberofmem = 2,
                                    activity_title = 'happy', budget =12,
                                    start_date =  datetime.date(2019,5,20),
                                    start_time = datetime.time(12,30,0),
                                    location = 'Waterloo',
                                    activity_content = "Happy day",
                                    Category = 1, 
                                    status = 3
                                    )

        Participant.objects.create(activity_id = activity, participant='1111111')
        Participant.objects.create(activity_id = activity, participant='2222222')
        #Participant.objects.create(activity_id = activity1, participant='3333333')

        self.client.post('/login',data=test_data2)

        #response = self.client.get('/activity')
        response = self.client.get(reverse('quit', kwargs={'activity_id': activity.activity_id}))

        #asset = Participant.objects.filter(activity_id=activity2.activity_id)
        asset = Participant.objects.values_list('participant', flat=True).filter(activity_id=activity.activity_id)

        activity = get_object_or_404(Activity, pk=activity.activity_id)
        status = activity.status

        self.assertEqual(response.status_code,302)
        #self.assertTemplateUsed('event.html')
        self.assertQuerysetEqual(list(asset), ["'1111111'"])
        self.assertEqual(status, 1)

