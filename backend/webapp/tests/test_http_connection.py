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
from webapp.models import Users, Products
logger = logging.getLogger(__name__)


# Create your tests here.

@pytest.mark.skip(reason="Disable test at develop")
class HttpServiceTC(unittest.TestCase):
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


    def TEST_post_a_file_to_http(self):
        """
        http upload file to api, file is located ".static"
        """
        with open('./client_assets/dog.jpg', 'rb') as file:
            r0 = self.client.post('http://localhost:8000/webapp/api/products/', {
                'title': 'test post', 'imageSource': file}, format='multipart')
            self.assertEqual(r0.data['title'], 'test post')
            self.assertEqual(r0.status_code, 201)
            r1 = self.client.delete(
                'http://localhost:8000/webapp/api/products/%s/' % r0.data['id'])
            self.assertEqual(r1.status_code, 204)

    def TEST_likeup_product(self):
        coll = [{
            "collectionName": "Apple %d" % randint(0, 9),
            "collectionDesc": "Apple desc %s" % (randint(0, 9))
        }]
        data = {
            'title': 'likeup',
            'collection': coll,
            'like': 100
        }
        r0 = self.client.post(
            'http://localhost:8000/webapp/api/products/', data, format='json')
        self.assertEqual(r0.data['like'], 100)
        r1 = self.client.put(
            'http://localhost:8000/webapp/api/products/%s/likeup/' % r0.data['id'])
        self.assertEqual(r1.status_code, 200)
        r2 = self.client.get(
            'http://localhost:8000/webapp/api/products/%s/' % r0.data['id'])
        self.assertEqual(r2.data['like'], 101)
        r3 = self.client.delete(
            'http://localhost:8000/webapp/api/products/%s/' % r0.data['id'])
        self.assertEqual(r3.status_code, 204)

    def TEST_likedown_product(self):
        coll = [{
            "collectionName": "Apple %d" % randint(0, 9),
            "collectionDesc": "Apple desc %s" % (randint(0, 9))
        }]
        data = {
            'title': 'likeup',
            'collection': coll,
            'like': 100
        }
        r0 = self.client.post(
            'http://localhost:8000/webapp/api/products/', data, format='json')
        self.assertEqual(r0.data['like'], 100)
        r1 = self.client.put(
            'http://localhost:8000/webapp/api/products/%s/likedown/' % r0.data['id'])
        self.assertEqual(r1.status_code, 200)
        r2 = self.client.get(
            'http://localhost:8000/webapp/api/products/%s/' % r0.data['id'])
        self.assertEqual(r2.data['like'], 99)
        r3 = self.client.delete(
            'http://localhost:8000/webapp/api/products/%s/' % r0.data['id'])
        self.assertEqual(r3.status_code, 204)

    def TEST_upload_file_product_then_delete_immediately(self):
        """
        test http post file product serializer
        """
        with open('./client_assets/dog.jpg', 'rb') as file:
            random = randint(0, 9)
            coll = [{
                "collectionName": "Apple %d" % random,
                "collectionDesc": "Apple desc %s" % random
            }]
            r0 = self.client.post('http://localhost:8000/webapp/api/products/', {
                'title': 'test post', 'collection': coll}, format='json')
            self.assertEqual(r0.data['collection'][0]
                             ['collectionName'], "Apple %d" % random)
            self.assertEqual(r0.status_code, 201)
            # Test get product details uploaded
            r1 = self.client.get(
                'http://localhost:8000/webapp/api/products/%s/' % r0.data['id'])

            self.assertEqual(r1.status_code, 200)
            # Test update field title product - use patch to update partial, put to update body
            newfile = open('./client_assets/index.jpg', 'rb')
            r3 = self.client.patch('http://localhost:8000/webapp/api/products/%s/' %
                                   r0.data['id'], {'imageSource': newfile}, format='multipart')
            self.assertEqual(r3.status_code, 200)
            # Test delete product uploaded
            r4 = self.client.delete(
                'http://localhost:8000/webapp/api/products/%s/' % r0.data['id'])
            # logger.debug(response.data)
            self.assertEqual(r4.status_code, 204)

    def TEST_upload_20_products(self):
        """
        test to upload 20 products in a short time
        """
        li = []
        for index in range(0, 20):
            with open('./client_assets/dog.jpg', 'rb') as file:
                coll = [{
                    "collectionName": "Apple %d" % randint(0, 9),
                    "collectionDesc": "Apple desc %s" % (randint(0, 9))
                }]
                views = randint(0, 10000)
                like = randint(0, 10000)
                price = randrange(10000, 1000000, 1000)
                r0 = self.client.post('http://localhost:8000/webapp/api/products/', {
                    'title': 'test post 1',  'collection': coll, 'views': views, 'like': like, 'price': price}, format='json')
                self.assertEqual(r0.data['price'], price)
                self.assertEqual(r0.status_code, 201)
                li.append(r0.data['id'])
        for index in li:
            r1 = self.client.delete(
                'http://localhost:8000/webapp/api/products/%s/' % index)
            self.assertEqual(r1.status_code, 204)

    def TEST_get_collection_name(self):
        """
        get list collection product, return a list
        """
        response = self.client.get(
            'http://localhost:8000/webapp/api/products/collection/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def TEST_add_20_users(self):
        """
        test to add 20 users to database
        """
        li = []
        for index in range(0, 20):
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
                r0 = self.client.post(
                    'http://localhost:8000/webapp/api/users/', data, format='multipart')
                self.assertEqual(r0.data['name'], 'user%d' % random)
                self.assertEqual(r0.data['avatar'], 'None')
                self.assertEqual(r0.status_code, 201)
                r1 = self.client.patch('http://localhost:8000/webapp/api/users/%s/' %
                                       r0.data['id'], {'avatar': file}, format='multipart')
                self.assertNotEqual(r1.data['avatar'], 'None')
                self.assertEqual(r1.status_code, 200)
                li.append(r0.data['id'])
        for index in li:
            r2 = self.client.delete(
                'http://localhost:8000/webapp/api/users/%s/' % index)
            self.assertEqual(r2.status_code, 204)

    def TEST_add_item_to_cart_list(self):
        """
        ability to add product object to user means items ready to pay
        """

        li = []
        for index in range(0, 3):
            coll = [{
                "collectionName": "Apple %d" % randint(0, 9),
                "collectionDesc": "Apple desc %s" % (randint(0, 9))
            }]
            views = randint(0, 10000)
            like = randint(0, 10000)
            price = randrange(10000, 1000000, 1000)
            data = {'title': 'test post 1', 'collection': coll,
                    'views': views, 'like': like, 'price': price}
            r0 = self.client.post(
                'http://localhost:8000/webapp/api/products/', data, format='json')
            self.assertEqual(r0.status_code, 201)
            self.assertEqual(r0.data['price'], price)
            self.assertEqual(r0.data['collection'], coll)
            li.append(r0.data['id'])

        product0 = li[0]
        product1 = li[1]
        product2 = li[2]

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
        r1 = self.client.post(
            'http://localhost:8000/webapp/api/users/', data, format='multipart')
        self.assertEqual(r1.data['name'], 'user%d' % random)
        self.assertEqual(r1.data['avatar'], 'None')
        self.assertEqual(r1.status_code, 201)
        _list = [{'_id': product0}, {'_id': product1}, {'_id': product2}]
        data = {'name': 'user1', 'email': 'user1@email.com', 'password': '12345678',
                'firstName': 'user1', 'lastName': 'user1', 'level': 1, 'group': 'cust', 'cartList': _list}
        responseu1 = self.client.put(
            'http://localhost:8000/webapp/api/users/%s/' % r1.data['id'], data, format='multipart')
        responseu2 = self.client.get(
            'http://localhost:8000/webapp/api/users/%s/' % r1.data['id'])
        self.assertEqual(responseu1.status_code, 200)
        r2 = self.client.delete(
            'http://localhost:8000/webapp/api/users/%s/' % r1.data['id'])
        self.assertEqual(r2.status_code, 204)
        for index in li:
            r3 = self.client.delete(
                'http://localhost:8000/webapp/api/products/%s/' % index)
            self.assertEqual(r3.status_code, 204)

    def TEST_update_payment_info(self):
        random = randint(0, 10000)
        pm = [{
            'cardBrand': 'Visa',
            'cardNumber': '112233445566778899'
        }]
        data = {
            'name': 'user%d' % random,
            'email': 'user%d@email.com' % random,
            'password': '12345678',
            'firstName': 'user%d' % random,
            'lastName': 'user%d' % random,
            'level': 1,
            'group': 'cust',
            'payment': pm
        }
        r0 = self.client.post(
            'http://localhost:8000/webapp/api/users/', data, format='json')
        self.assertEqual(r0.data['payment'][0]['cardBrand'], 'Visa')
        self.assertEqual(r0.status_code, 201)
        r1 = self.client.delete(
            'http://localhost:8000/webapp/api/users/%s/' % r0.data['id'])
        self.assertEqual(r1.status_code, 204)

    def TEST_reference_field_cascade(self):
        coll = [{
            "collectionName": "Apple %d" % randint(0, 9),
            "collectionDesc": "Apple desc %s" % (randint(0, 9))
        }]
        data = {
            'title': 'likeup',
            'collection': coll,
            'like': 100
        }
        p0 = self.client.post(
            'http://localhost:8000/webapp/api/products/', data, format='json')
        self.assertEqual(p0.status_code, 201)
        p1 = self.client.post(
            'http://localhost:8000/webapp/api/products/', data, format='json')
        self.assertEqual(p1.status_code, 201)
        p2 = self.client.post(
            'http://localhost:8000/webapp/api/products/', data, format='json')
        self.assertEqual(p2.status_code, 201)
        list_product = [{'_id': p0.data['id']}, {'_id': p1.data['id']}, {'_id': p2.data['id']}]
        random = randint(0,100)
        data = {
            'name': 'user%d' % random,
            'email': 'user%d@email.com' % random,
            'password': '12345678',
            'firstName': 'user%d' % random,
            'lastName': 'user%d' % random,
            'level': 1,
            'group': 'cust'
        }
        u0 = self.client.post(
            'http://localhost:8000/webapp/api/users/', data, format='multipart')
        self.assertEqual(u0.status_code, 201)        
        data = {'name': 'TEST_reference_field_cascade', 'email': 'user1@email.com', 'password': '12345678',
                'firstName': 'user1', 'lastName': 'user1', 'level': 1, 'group': 'cust', 'cartList': list_product}
        u1 = self.client.put('http://localhost:8000/webapp/api/users/%s/' %u0.data['id'], data, format='multipart')
        self.assertEqual(u1.status_code, 200)
        before_del = self.client.get('http://localhost:8000/webapp/api/users/')
        self.assertEqual(before_del.status_code, 200)
        self.assertEqual(len(before_del.data['results'][0]['cartList']), 3)
        # delete 1 product then check if exist in users, test case is failed
        u2 = self.client.delete('http://localhost:8000/webapp/api/products/%s/' %p0.data['id'])
        self.assertEqual(u2.status_code, 204)
        after_del = self.client.get('http://localhost:8000/webapp/api/users/')
        self.assertEqual(after_del.status_code, 200)
        self.assertEqual(len(after_del.data['results'][0]['cartList']),2)
        # cleanup products
        for index in list_product:
            r = self.client.get('http://localhost:8000/webapp/api/products/%s/' % index['_id'])
            if r.status_code == 200:
                self.client.delete('http://localhost:8000/webapp/users/%s/' %index['_id'])
        # cleanup user
        self.client.delete('http://localhost:8000/webapp/api/users/%s/'%u0.data['id'])
    def test_singlr_reference(self):
        coll = [{
            "collectionName": "Apple %d" % randint(0, 9),
            "collectionDesc": "Apple desc %s" % (randint(0, 9))
        }]
        data = {
            'title': 'likeup',
            'collection': coll,
            'like': 100
        }
        p0 = self.client.post(
            'http://localhost:8000/webapp/api/products/', data, format='json')
        self.assertEqual(p0.status_code, 201)
        list_product = {'_id': p0.data['id']}
        random = randint(0,100)
        data = {'name': 'TEST_reference_field_cascade', 'email': 'user1@email.com', 'password': '12345678',
                'firstName': 'user1', 'lastName': 'user1', 'level': 1, 'group': 'cust', 'cartList': list_product}
        u1 = self.client.post('http://localhost:8000/webapp/api/users/', data, format='json')
        self.assertEqual(u1.status_code, 201)
        u2 = self.client.get('http://localhost:8000/webapp/api/users/%s/' % u1.data['id'])
        self.assertEqual(u2.status_code, 200)
        self.assertNotEqual(u2.data['cartList'], None)

    def doCleanups(self):
        Users.drop_collection()
        Products.drop_collection()