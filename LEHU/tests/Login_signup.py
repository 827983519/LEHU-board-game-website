from django.test import TestCase
from LEHU.models import User,Activity,Participant
from LEHU.views import loginForm,registerForm
import json
from django.contrib.auth.hashers import make_password, check_password
import datetime
from django.test.client import Client



class LoginActionTest(TestCase):
    def setUp(self):
        User.objects.create(user_username = '827983519',
                           user_password = make_password('a827983519'),
                           user_email = '827983519@qq.com',
                           user_gender = 'Male',)


    def test_username_password_none(self):
        test_data = {'username':'','password':'' }
        response = self.client.post('/login',data=test_data)
        result = json.loads(response.content)
        self.assertEqual(result['user'],'fail')


    def test_username_password_wrong(self):
        test_data = {'username':'827983519','password':'a819' }
        response = self.client.post('/login',data=test_data)
        result = json.loads(response.content)
        self.assertEqual(result['user'],'fail')


    def test_username_password_correct(self):
        test_data = {'username':'827983519','password': 'a827983519' }
        response = self.client.post('/login',data=test_data)
        result = json.loads(response.content)
        self.assertEqual(result['user'],'success')




class SignupActionTest(TestCase):
    def setUp(self):
        User.objects.create(user_username = '827983519',
                           user_password = make_password('a827983519'),
                           user_email = '827983519@qq.com',
                           user_gender = 'Male',)

    def test_signup_page(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed('register_new.html')

    def test_signup_username_wrong_format(self):
        test_data = {'username':"a",'password':'a827983519','confirmPassword':'a827983519','email':'827983519@qq.com','gender':'Male'}
        response = self.client.post('/register',data=test_data)
        result = json.loads(response.content)
        self.assertEqual(result['register'],'fail')
        self.assertEqual(result['msg'],'Username and password length need to be between 6 to 20.')

    def test_signup_password_wrong_format(self):
        test_data = {'username':"a2332423412",'password':'a','confirmPassword':'a827983519','email':'827983519@qq.com','gender':'Male'}
        response = self.client.post('/register',data=test_data)
        result = json.loads(response.content)
        self.assertEqual(result['register'],'fail')
        self.assertEqual(result['msg'],'Username and password length need to be between 6 to 20.')

    def test_signup_password_Confirmpassword_inconsistent(self):
        test_data = {'username':"assadasd",'password':'a827983519','confirmPassword':'sssssddqwqe','email':'827983519@qq.com','gender':'Male'}
        response = self.client.post('/register',data=test_data)
        result = json.loads(response.content)
        self.assertEqual(result['register'],'fail')
        self.assertEqual(result['msg'],'Inconsistent password entered')

    def test_signup_email_exist(self):
        test_data = {'username':"assadasd",'password':'a827983519','confirmPassword':'a827983519','email':'827983519@qq.com','gender':'Male'}
        response = self.client.post('/register',data=test_data)
        result = json.loads(response.content)
        self.assertEqual(result['register'],'fail')
        self.assertEqual(result['msg'],'This Email has been used')

    def test_signup_username_exist(self):
        test_data = {'username':"827983519",'password':'a827983519','confirmPassword':'a827983519','email':'8283519@qq.com','gender':'Male'}
        response = self.client.post('/register',data=test_data)
        result = json.loads(response.content)
        self.assertEqual(result['register'],'fail')
        self.assertEqual(result['msg'],'Usename already exists')


    def test_signup_email_wrong_format(self):
        test_data = {'username':"8279183519",'password':'a827983519','confirmPassword':'a827983519','email':'8283q.com','gender':'Male'}
        response = self.client.post('/register',data=test_data)
        result = json.loads(response.content)
        self.assertEqual(result['register'],'fail')
        self.assertEqual(result['msg'],'Wrong input format')

    def test_signup_correct(self):
        test_data = {'username':"8279183519a",'password':'a827983519','confirmPassword':'a827983519','email':'828323423@qq.com','gender':'Male'}
        response = self.client.post('/register',data=test_data)
        result = json.loads(response.content)
        self.assertEqual(result['register'],'success')
        a = User.objects.all()
        self.assertEqual(len(a),2)
