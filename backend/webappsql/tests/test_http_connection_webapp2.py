"""
declare simple testcase, only http test still now
"""
import json
import time
import unittest
import logging
import bson
import pytest
from collections import MutableMapping, OrderedDict
from random import randint, randrange
from rest_framework.test import APIClient
logger = logging.getLogger(__name__)


# Create your tests here.

@pytest.mark.skip(reason="Disable test at develop")
class HttpServiceTCWebapp2(unittest.TestCase):
    """
    Testcases to validate http service usage, use rest framework api test
    """

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

    def test_post_a_file_to_http(self):
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
                self.assertEqual(r0,'')
                self.assertEqual(r0.status_code, 201)
