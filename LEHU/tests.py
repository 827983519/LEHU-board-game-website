from ./test/tests import LoginActionTest
# from django.test import TestCase
# from LEHU.models import User,Activity,Participant
# from LEHU.views import loginForm,registerForm
# import json
# from django.contrib.auth.hashers import make_password, check_password
# import datetime
# from django.test.client import Client
#
#
#
# class LoginActionTest(TestCase):
#     def setUp(self):
#         User.objects.create(user_username = '827983519',
#                            user_password = make_password('a827983519'),
#                            user_email = '827983519@qq.com',
#                            user_gender = 'Male',)
#
#
#     def test_username_password_none(self):
#         test_data = {'username':'','password':'' }
#         response = self.client.post('/login',data=test_data)
#         result = json.loads(response.content)
#         self.assertEqual(result['user'],'fail')
#
#
#     def test_username_password_wrong(self):
#         test_data = {'username':'827983519','password':'a819' }
#         response = self.client.post('/login',data=test_data)
#         result = json.loads(response.content)
#         self.assertEqual(result['user'],'fail')
#
#
#     def test_username_password_correct(self):
#         test_data = {'username':'827983519','password': 'a827983519' }
#         response = self.client.post('/login',data=test_data)
#         result = json.loads(response.content)
#         self.assertEqual(result['user'],'success')
#
#
#
#
# class SignupActionTest(TestCase):
#     def setUp(self):
#         User.objects.create(user_username = '827983519',
#                            user_password = make_password('a827983519'),
#                            user_email = '827983519@qq.com',
#                            user_gender = 'Male',)
#
#     def test_signup_page(self):
#         response = self.client.get('/register')
#         self.assertEqual(response.status_code,200)
#         self.assertTemplateUsed('register_new.html')
#
#     def test_signup_username_wrong_format(self):
#         test_data = {'username':"a",'password':'a827983519','confirmPassword':'a827983519','email':'827983519@qq.com','gender':'Male'}
#         response = self.client.post('/register',data=test_data)
#         result = json.loads(response.content)
#         self.assertEqual(result['register'],'fail')
#         self.assertEqual(result['msg'],'Username and password length need to be between 6 to 20.')
#
#     def test_signup_password_wrong_format(self):
#         test_data = {'username':"a2332423412",'password':'a','confirmPassword':'a827983519','email':'827983519@qq.com','gender':'Male'}
#         response = self.client.post('/register',data=test_data)
#         result = json.loads(response.content)
#         self.assertEqual(result['register'],'fail')
#         self.assertEqual(result['msg'],'Username and password length need to be between 6 to 20.')
#
#     def test_signup_password_Confirmpassword_inconsistent(self):
#         test_data = {'username':"assadasd",'password':'a827983519','confirmPassword':'sssssddqwqe','email':'827983519@qq.com','gender':'Male'}
#         response = self.client.post('/register',data=test_data)
#         result = json.loads(response.content)
#         self.assertEqual(result['register'],'fail')
#         self.assertEqual(result['msg'],'Inconsistent password entered')
#
#     def test_signup_email_exist(self):
#         test_data = {'username':"assadasd",'password':'a827983519','confirmPassword':'a827983519','email':'827983519@qq.com','gender':'Male'}
#         response = self.client.post('/register',data=test_data)
#         result = json.loads(response.content)
#         self.assertEqual(result['register'],'fail')
#         self.assertEqual(result['msg'],'This Email has been used')
#
#     def test_signup_username_exist(self):
#         test_data = {'username':"827983519",'password':'a827983519','confirmPassword':'a827983519','email':'8283519@qq.com','gender':'Male'}
#         response = self.client.post('/register',data=test_data)
#         result = json.loads(response.content)
#         self.assertEqual(result['register'],'fail')
#         self.assertEqual(result['msg'],'Usename already exists')
#
#
#     def test_signup_email_wrong_format(self):
#         test_data = {'username':"8279183519",'password':'a827983519','confirmPassword':'a827983519','email':'8283q.com','gender':'Male'}
#         response = self.client.post('/register',data=test_data)
#         result = json.loads(response.content)
#         self.assertEqual(result['register'],'fail')
#         self.assertEqual(result['msg'],'Wrong input format')
#
#     def test_signup_correct(self):
#         test_data = {'username':"8279183519a",'password':'a827983519','confirmPassword':'a827983519','email':'828323423@qq.com','gender':'Male'}
#         response = self.client.post('/register',data=test_data)
#         result = json.loads(response.content)
#         self.assertEqual(result['register'],'success')
#         a = User.objects.all()
#         self.assertEqual(len(a),2)
#
#
# class MainpageTest(TestCase):
#     pass
#
#
#
# class NoLoginTest(TestCase):
#     def test_activity_nologin(self):
#         response = self.client.get('/activity')
#         self.assertEqual(response.status_code,302)
#         self.assertTemplateUsed('activities.html')
#
#     def test_profile_nologin(self):
#         response = self.client.get('/profile')
#         self.assertEqual(response.status_code,302)
#         self.assertTemplateUsed('profile.html')
#
#     def test_activity_nologin(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code,302)
#         self.assertTemplateUsed('index_new.html')
#
#     def test_message_nologin(self):
#         response = self.client.get('/message')
#         self.assertEqual(response.status_code,302)
#         self.assertTemplateUsed('Unread.html')
#
#     def test_post_nologin(self):
#         response = self.client.get('/post')
#         self.assertEqual(response.status_code,302)
#         self.assertTemplateUsed('post.html')
#
#     def test_search_nologin(self):
#         response = self.client.get('/search')
#         self.assertEqual(response.status_code,302)
#         self.assertTemplateUsed('search.html')
#
#
#
# class ActivityTest(TestCase):
#     def setUp(self):
#
#         test_data = {'username':'827983519','password': 'a827983519' }
#
#         # Activity.objects.create(owner = '827983519',numberofmem = 10,
#         #                             activity_title = 'happy', budget =12,
#         #                             start_date =  datetime.date(2019,5,20),
#         #                             start_time = datetime.time(12,30,0),
#         #                             location = 'Waterloo',
#         #                             activity_content = "Happy day",
#         #                             Category = 1)
#
#         User.objects.create(user_username = '827983519',
#                            user_password = make_password('a827983519'),
#                            user_email = '827983519@qq.com',
#                            user_gender = 'Male',)
#
#         self.client = Client()
#         self.client.post('/login',data=test_data)
#
#     def test_activity_login(self):
#         response = self.client.get('/activity')
#         self.assertEqual(response.status_code,200)
#         self.assertTemplateUsed('activities.html')
#
#     def test_activity_no_activity(self):
#         response = self.client.get('/activity')
#         self.assertEqual(response.status_code,200)
#         self.assertTemplateUsed('activities.html')
#         self.assertContains(response,'[Activities not attended]')
#         self.assertContains(response,'[No host activity]')
#
#     def test_activity_1host_activity(self):
#         Activity.objects.create(owner = '827983519',numberofmem = 10,
#                                     activity_title = 'happy', budget =12,
#                                     start_date =  datetime.date(2019,5,20),
#                                     start_time = datetime.time(12,30,0),
#                                     location = 'Waterloo',
#                                     activity_content = "Happy day",
#                                     Category = 1, status=1)
#         Participant.objects.create()
#
#         response = self.client.get('/activity')
#         self.assertEqual(response.status_code,200)
#         self.assertTemplateUsed('activities.html')
#         self.assertContains(response,'[Activities not attended]')
#         self.assertContains(response,'[happy]')
#         self.assertContains(response,'Open')
#         self.assertContains(response, datetime.date(2019,5,20).strftime('%B %d, %Y'))
#         self.assertContains(response, datetime.time(12,30,0).strftime('%H:%M'))
#
#
#
#     def test_activity_1register_activity(self):
#         Activity.objects.create(owner = '827983519a',numberofmem = 10,
#                                     activity_title = 'happy', budget =12,
#                                     start_date =  datetime.date(2019,5,20),
#                                     start_time = datetime.time(12,30,0),
#                                     location = 'Waterloo',
#                                     activity_content = "Happy day",
#                                     Category = 1, status=1)
#
#         response = self.client.get('/activity')
#         self.assertEqual(response.status_code,200)
#         self.assertTemplateUsed('activities.html')
#         self.assertContains(response,'[No host activity]')
#         self.assertContains(response,'[happy]')
#         self.assertContains(response,'Open')
#         self.assertContains(response, datetime.date(2019,5,20).strftime('%B %d, %Y'))
#         self.assertContains(response, datetime.time(12,30,0).strftime('%H:%M'))
#
#
#
#
#
# class ProfileTest(TestCase):
#     pass
#
#
# class MessageTest(TestCase):
#     pass
#
#
# class PostTest(TestCase):
#     pass
#
#
# class SearchTest(TestCase):
#     pass
