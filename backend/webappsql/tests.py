import logging
import pytest
from random import randint
from rest_framework.test import APIClient
from django.test import TestCase

logger = logging.getLogger(__name__)
# Create your tests here.
class TestWebapp2(TestCase):
    def setUp(self):
        """
        Setting up testcases
        """
        self.client = APIClient()

    def tearDown(self):
        """
        Cleanup testcases when complete
        """
        del self.client

    def test_webapp2(self):
        """
        http upload file to api
        """
        for index in range(1,100):
            rand = randint(1,100)
            with open('./client_assets/dog.jpg', 'rb') as file:
                data = {
                    'title': f'product {rand}',
                    'simpleDesc': f'product desc {rand}',
                    'fullDesc': f'product full desc {rand}',
                    'price': rand,
                    'like': rand,
                    'imageSource': file,
                    'discount': f'product sale {rand}'
                }
                r0 = self.client.post('http://localhost:8000/webapp2/api/product/', data, format='multipart')
                logger.debug(r0.data)
                self.assertEqual(r0.status_code, 201)

    def test_file_is_deleted_correctly_on_system_when_product_deletion_occurs(self):
        """This test case will validate file field in model product before/after deletion, 
        file should exists before and not exists after deletion
        """
        pass

    def test_old_file_is_deleted_correctly_on_system_when_product_deletion_occurs(self):
        """This test case will validate file field in model product before/after updating,
        old file should be deleted out of system and new file should exists
        """
        pass