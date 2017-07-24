"""
declare simple testcase, only http test still now
"""
import json
import time
import unittest
import logging
import bson
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

    def TEST_credential_user_administrator(self):
        """
        Test ability to login user role administrator
        """
        user = {
            "email": "user1@email.com",
            "password": "12345678",
            "username": "user1",
            "group": "admin"
        }
        response = self.client.post(
            'http://localhost:8000/webapp/api/users/login/', data=user)
        logger.debug(response.data)
        self.assertEqual(response.status_code, 200)

    def TEST_credential_user_customer_but_failed(self):
        """
        Test ability to login user role customer but failed
        """
        user = {
            "email": "user1@email.com",
            "password": "12345678",
            "username": "user1",
            "group": "customer"
        }
        userdumps = json.dumps(user)
        # logger.debug(userdumps)
        response = self.client.post(
            'http://localhost:8000/webapp/api/users/login/', data=user)
        logger.debug(response.data)
        self.assertEqual(response.status_code, 200)

    def TEST_get_list_group_user(self):
        """
        get list of group users
        """
        response = self.client.get(
            'http://localhost:8000/webapp/api/users/group_user/')
        logger.debug(response.data)
        self.assertIn("admin", response.data)
        self.assertEqual(response.status_code, 200)

    def TEST_post_a_file_to_http(self):
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
            # logger.debug(response.data)
            self.assertEqual(response.status_code, 201)

    def TEST_upload_file_product_then_delete_immediately(self):
        """
        test http post file product serializer
        """
        with open('./client_assets/dog.jpg', 'rb') as file:
            coll = json.dumps({
                "collectionName": "Apple %d" % randint(0, 9),
                "collectionDesc": "Apple desc %s" % (randint(0, 9))
            })
            response = self.client.post('http://localhost:8000/webapp/api/products/', {
                                        'title': 'test post', 'imageSource': file, 'collection': coll}, format='multipart')
            # logger.debug(response.data)
            postID = response.data['id']
            self.assertEqual(response.status_code, 201)
            # Test get product details uploaded
            response = self.client.get(
                'http://localhost:8000/webapp/api/products/%s/' % postID)
            # logger.debug(response.data)
            self.assertEqual(response.status_code, 200)
            # Test get imageSource from Product viewSet
            response = self.client.get(
                'http://localhost:8000/webapp/api/products/%s/image/' % postID)
            self.assertEqual(response.status_code, 200)
            # Test update field title product - use patch to update partial, put to update body
            newfile = open('./client_assets/index.jpg', 'rb')
            response = self.client.patch('http://localhost:8000/webapp/api/products/%s/' %
                                         postID, {'imageSource': newfile}, format='multipart')
            self.assertEqual(response.status_code, 200)
            # Test delete product uploaded
            response = self.client.delete(
                'http://localhost:8000/webapp/api/products/%s/' % postID)
            # logger.debug(response.data)
            self.assertEqual(response.status_code, 204)

    def TEST_upload_20_products(self):
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
            # logger.debug(response.data)
            self.assertEqual(response.status_code, 201)

    def TEST_get_list_all_product(self):
        response = self.client.get(
            'http://localhost:8000/webapp/api/products/')
        # logger.debug(response.data)
        self.assertEqual(response.status_code, 200)

    def TEST_get_collection_name(self):
        """
        get list collection product by distinct method mongoengine
        """
        response = self.client.get(
            'http://localhost:8000/webapp/api/products/collection/')
        # logger.debug(response.data)
        self.assertEqual(response.status_code, 200)

    def TEST_add_200_users(self):
        """
        test to add 200 users in a short time
        """
        for index in range(0, 200):
            with open('./client_assets/dog.jpg', 'rb') as file:
                random = randint(0, 10000)
                data = {
                    'name': 'user%d' % random,
                    'email': 'user%d@email.com' % random,
                    'password': '12345678',
                    'firstName': 'user%d' % random,
                    'lastName': 'user%d' % random,
                    'level': 1,
                    'group': 'cust'
                }
                response = self.client.post(
                    'http://localhost:8000/webapp/api/users/', data, format='multipart')
                self.assertEqual(response.status_code, 201)
                id = response.data['id']
                response = self.client.patch('http://localhost:8000/webapp/api/users/%s/' %
                                             id, {'avatar': file}, format='multipart')
                self.assertEqual(response.status_code, 200)

    def test_add_item_to_cart_list(self):
        """
        ability to add product object to user means items ready to pay
        """
        responsep0 = self.client.get(
            'http://localhost:8000/webapp/api/products/')
        self.assertEqual(responsep0.status_code, 200)
        product0 = responsep0.data['results'][0]
        product1 = responsep0.data['results'][1]
        product2 = responsep0.data['results'][2]
        users = self.client.get(
            'http://localhost:8000/webapp/api/users/')
        responseu0 = self.client.get(
            'http://localhost:8000/webapp/api/users/{userid}/'.format(userid=users.data['results'][0]['id']))
        self.assertEqual(responseu0.status_code, 200)
        user0 = responseu0.data
        _list = [{'_id': product0['id']},{'_id': product1['id']},{'_id': product2['id']}]

        responseu1 = self.client.patch(
            'http://localhost:8000/webapp/api/users/%s/' % user0['id'], {'cartList': _list}, format='json')
        responseu2 = self.client.get(
            'http://localhost:8000/webapp/api/users/%s/' % user0['id'])
        logger.debug(responseu1.data)
        self.assertEqual(responseu1.status_code, 200)
