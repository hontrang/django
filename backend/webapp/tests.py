"""
declare simple testcase, only http test still now
"""
import json
import time
import unittest
import logging
from random import randint, randrange

from rest_framework.test import APIClient
logger = logging.getLogger(__name__)


# Create your tests here.


class HttpServiceTestCase(unittest.TestCase):
    """
    Testcases to validate http service usage, use rest framework api test
    """

    def setUp(self):
        """
        Setting up testcases
        """
        # print('=========== ROOT DIR ============')
        # show list items in directory
        # print(os.listdir())
        self.client = APIClient()


    def tearDown(self):
        """
        Cleanup testcases when complete
        """
        del self.client

    def test_credential_user_administrator(self):
        """
        Test ability to login user role administrator
        """
        user = {
            "email":"user1@email.com",
            "password": "12345678",
            "username": "user1",
            "group": "admin"
        }
        userdumps = json.dumps(user)
        #logger.debug(userdumps)
        response = self.client.post('http://localhost:8000/webapp/api/users/login/',data = user)
        logger.debug(response.data)
        self.assertEqual(response.status_code, 200)

    def test_credential_user_customer_but_failed(self):
        """
        Test ability to login user role customer but failed
        """
        user = {
            "email":"user1@email.com",
            "password": "12345678",
            "username": "user1",
            "group": "customer"
        }
        userdumps = json.dumps(user)
        #logger.debug(userdumps)
        response = self.client.post('http://localhost:8000/webapp/api/users/login/',data = user)
        logger.debug(response.data)
        self.assertEqual(response.status_code, 400)
    def test_get_list_group_user(self):
        """
        get list of group users
        """
        response = self.client.get('http://localhost:8000/webapp/api/users/group_user/')
        logger.debug(response.data)
        self.assertIn("admin", response.data)
        self.assertEqual(response.status_code, 200)

    def test_post_a_file_to_http(self):
        """
        http upload file to api, file is located ".static"
        """
        with open('./client_assets/dog.jpg', 'rb') as file:
            coll = json.dumps({
                "collectionName": "Apple %d" % randint(0, 9),
                "collectionDesc": "Apple desc %s" % (randint(0, 9))
            })
            response = self.client.post('http://localhost:8000/webapp/api/products/', {
                                        'title': 'test post', 'imageSource': file, 'collection': coll}, format='multipart')
            #logger.debug(response.data)
            self.assertEqual(response.status_code, 201)

    def test_upload_file_product_then_delete_immediately(self):
        """
        test http post file product serializer
        """
        with open('./client_assets/dog.jpg', 'rb') as file:
            coll = json.dumps({
                "collectionName": "Apple %d" % randint(0, 9),
                "collectionDesc": "Apple desc %s" % (randint(0, 9))
            })
            response = self.client.post('http://localhost:8000/webapp/api/products/', {
                                        'title': 'test post', 'imageSource': file, 'collection': coll},format='multipart')
            #logger.debug(response.data)
            postID = response.data['id']
            self.assertEqual(response.status_code, 201)
            # Test get product details uploaded
            response = self.client.get(
                'http://localhost:8000/webapp/api/products/%s/' % postID)
            #logger.debug(response.data)
            self.assertEqual(response.status_code, 200)
            # Test get imageSource from Product viewSet
            response = self.client.get(
                'http://localhost:8000/webapp/api/products/%s/image/' % postID)
            self.assertEqual(response.status_code, 200)
            # Test update field title product - use patch to update partial, put to update body
            newfile = open('./client_assets/index.jpg','rb')
            response = self.client.patch('http://localhost:8000/webapp/api/products/%s/' % postID, {'imageSource': newfile}, format='multipart')
            self.assertEqual(response.status_code, 200)
            # Test delete product uploaded
            response = self.client.delete(
                'http://localhost:8000/webapp/api/products/%s/' % postID)
            #logger.debug(response.data)
            self.assertEqual(response.status_code, 204)

    def test_upload_20_products(self):
        """
        test to upload 20 products in a short time
        """
        for index in range(0, 20):
            with open('./client_assets/dog.jpg', 'rb') as file:
                coll = json.dumps({
                    "collectionName": "Apple %d" % randint(0, 9),
                    "collectionDesc": "Apple desc %s" % (randint(0, 9))
                })
                views = randint(0, 10000)
                like = randint(0, 10000)
                price = randrange(10000, 1000000, 1000)
                response = self.client.post('http://localhost:8000/webapp/api/products/', {
                                            'title': 'test post 1', 'imageSource': file, 'collection': coll, 'views': views, 'like': like, 'price': price}, format='multipart')
            #logger.debug(response.data)
            self.assertEqual(response.status_code, 201)

    def test_get_list_all_product(self):
        response = self.client.get(
            'http://localhost:8000/webapp/api/products/')
        #logger.debug(response.data)
        self.assertEqual(response.status_code, 200)


    def test_get_collection_name(self):
        """
        get list collection product by distinct method mongoengine
        """
        response = self.client.get(
            'http://localhost:8000/webapp/api/products/collection/')
        #logger.debug(response.data)
        self.assertEqual(response.status_code, 200)
