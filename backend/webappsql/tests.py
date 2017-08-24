import logging
import pytest
from random import randint
from rest_framework.test import APIClient
from django.test import TestCase
from .views import CustomerViewSet, ProductViewSet
from webappsql.utils import translate_testserver_to_localhost
import time
import requests
logger = logging.getLogger(__name__)
# Create your tests here.
class TestWebapp2(TestCase):
    def setUp(self):
        """
        Setting up testcases
        """
        self.client = APIClient()
        self.file = open('./client_assets/index.jpg', 'rb')
        self.file1 = open('./client_assets/dog.jpg', 'rb')

    def tearDown(self):
        """
        Cleanup testcases when complete
        """
        del self.client

    def test_file_is_deleted_correctly_on_system_when_user_deletion_occurs(self):
        """This test case will validate file field in model user before/after deletion, 
        file should exists before and not exists after deletion
        """
        rand = randint(1,10)
        user = {
          'name': 'khach hang %d' %rand,
          'email': 'khachhang%d@email.com' %rand,
          'password': '123456789',
          'firstName': 'khach',
          'lastName': 'hang %d' %rand,
          'avatar': (self.file.name,self.file),
          'level': '%d' %1,
          'group':  'cust',
        }
        r0 = self.client.post('http://localhost:8000/webapp2/api/user/', user, format='multipart')
        self.assertEqual(r0.status_code, 201)
        self.assertIsNotNone(r0.data['avatar'])
        r1 = self.client.delete('http://localhost:8000/webapp2/api/user/%s/' %r0.data['id'])
        self.assertEqual(r1.status_code, 204)
        a2 = requests.get(translate_testserver_to_localhost(r0.data['avatar']))
        self.assertEqual(a2.status_code, 404)

    def test_old_file_is_deleted_correctly_on_system_when_user_updating_occurs(self):
        """This test case will validate file field in model user before/after updating,
        old file should be deleted out of system and new file should exists
        """
        rand = randint(1,10)
        user0 = {
          'name': 'khach hang %d' %rand,
          'email': 'khachhang%d@email.com' %rand,
          'password': '123456789',
          'firstName': 'khach',
          'lastName': 'hang %d' %rand,
          'avatar': (self.file.name,self.file),
          'level': '%d' %1,
          'group':  'cust',
        }
        user1 = {
          'name': 'khach hang %d' %rand,
          'email': 'khachhang%d@email.com' %rand,
          'password': '123456789',
          'firstName': 'khach',
          'lastName': 'hang %d' %rand,
          'avatar': (self.file1.name,self.file1),
          'level': '%d' %1,
          'group':  'cust',
        }
        r0 = self.client.post('http://localhost:8000/webapp2/api/user/', user0 , format='multipart')
        self.assertEqual(r0.status_code, 201)
        self.assertIsNotNone(r0.data['avatar'])
        # APIClient always returns 404 not found, use requests library instead
        a1 = requests.get(translate_testserver_to_localhost(r0.data['avatar']))
        self.assertEqual(a1.status_code, 200)
        r1 = self.client.put('http://localhost:8000/webapp2/api/user/%s/' %r0.data['id'], user1, format='multipart')
        self.assertEqual(r1.status_code, 200)
        self.assertIsNotNone(r1.data['avatar'])
        self.assertNotEqual(r0.data['avatar'], r1.data['avatar'])
        # APIClient always returns 404 not found, use requests library instead
        a2 = requests.get(translate_testserver_to_localhost(r0.data['avatar']))
        self.assertEqual(a2.status_code, 404)
        # APIClient always returns 404 not found, use requests library instead
        a3 = requests.get(translate_testserver_to_localhost(r1.data['avatar']))
        self.assertEqual(a3.status_code, 200)
        r2 = self.client.delete('http://localhost:8000/webapp2/api/user/%s/' %r0.data['id'])
        self.assertEqual(r2.status_code, 204)
        a4 = requests.get(translate_testserver_to_localhost(r1.data['avatar']))
        self.assertEqual(a4.status_code, 404)

    def test_file_still_existing_when_update_user_without_avatar(self):
        """This test case will validate when user updating without avatar field, 
        image file in system must still exist
        """
        rand = randint(1,10)
        user0 = {
          'name': 'khach hang %d' %rand,
          'email': 'khachhang%d@email.com' %rand,
          'password': '123456789',
          'firstName': 'khach',
          'lastName': 'hang %d' %rand,
          'avatar': (self.file.name,self.file),
          'level': '%d' %1,
          'group':  'cust',
        }
        user1 = {
          'name': 'khach hang %d updated' %rand,
        }
        r0 = self.client.post('http://localhost:8000/webapp2/api/user/', user0, format='multipart')
        self.assertEqual(r0.status_code, 201)
        a0= requests.get(translate_testserver_to_localhost(r0.data['avatar']))
        self.assertEqual(a0.status_code, 200)
        r1 = self.client.patch('http://localhost:8000/webapp2/api/user/%s/' %r0.data['id'], user1)
        self.assertEqual(r1.status_code, 200)
        a1 = requests.get(translate_testserver_to_localhost(r1.data['avatar']))
        self.assertEqual(a1.status_code, 200)
        r2 = self.client.delete('http://localhost:8000/webapp2/api/user/%s/' %r0.data['id'])
        self.assertEqual(r2.status_code, 204)


