from django.test import TestCase
from LEHU.models import User,Activity,Participant
from LEHU.views import loginForm,registerForm
import json
from django.contrib.auth.hashers import make_password, check_password
import datetime
from django.test.client import Client



class NoLoginTest(TestCase):
    def test_activity_nologin(self):
        response = self.client.get('/activity')
        self.assertEqual(response.status_code,302)
        self.assertTemplateUsed('activities.html')

    def test_profile_nologin(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code,302)
        self.assertTemplateUsed('profile.html')

    def test_activity_nologin(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,302)
        self.assertTemplateUsed('index_new.html')

    def test_message_nologin(self):
        response = self.client.get('/message')
        self.assertEqual(response.status_code,302)
        self.assertTemplateUsed('Unread.html')

    def test_post_nologin(self):
        response = self.client.get('/post')
        self.assertEqual(response.status_code,302)
        self.assertTemplateUsed('post.html')

    def test_search_nologin(self):
        response = self.client.get('/search')
        self.assertEqual(response.status_code,302)
        self.assertTemplateUsed('search.html')
