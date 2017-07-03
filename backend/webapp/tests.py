"""
declare simple testcase, only http test still now
"""
import json
from random import randint, randrange

# import os
from django.test import Client
import unittest


# Create your tests here.


class HttpServiceTestCase(unittest.TestCase):
    """
    Testcases to validate http service usage
    """

    def setUp(self):
        """
        Setting up testcases
        """
        # print('=========== ROOT DIR ============')
        # show list items in directory
        # print(os.listdir())
        self.client = Client()
        BOUNDARY = 'BoUnDaRyStRiNg'
        self.MULTIPART_CONTENT = 'multipart/form-data; boundary=%s' % BOUNDARY

    def tearDown(self):
        """
        Cleanup testcases when complete
        """
        del self.client

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
                                        'title': 'test post', 'imageSource': file, 'collection': coll})
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
                                        'title': 'test post', 'imageSource': file, 'collection': coll})
            postID = response.data['id']
            self.assertEqual(response.status_code, 201)
            # Test get product details uploaded
            response = self.client.get(
                'http://localhost:8000/webapp/api/products/%s/' % postID)
            self.assertEqual(response.status_code, 200)
            # Test get imageSource field upLoaded
            response = self.client.get(
                'http://localhost:8000/webapp/api/static-image/%s/' % postID)
            self.assertEqual(response.status_code, 200)
            # Test get imageSource from Product viewSet
            response = self.client.get(
                'http://localhost:8000/webapp/api/products/%s/image/' % postID)
            self.assertEqual(response.status_code, 200)
            # Test update field title product
            # response = self.client.put('http://localhost:8000/webapp/api/products/%s/' % postID, {
            #     'title': 'test put put', 'imageSource': file, 'collection': coll}, content_type=self.MULTIPART_CONTENT, format='multipart')
            # self.assertEqual(response.status_code, 200)
            # Test delete product uploaded
            response = self.client.delete(
                'http://localhost:8000/webapp/api/products/%s/' % postID)
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
            self.assertEqual(response.status_code, 201)

    def test_get_list_all_product(self):
        response = self.client.get(
            'http://localhost:8000/webapp/api/products/')
        self.assertEqual(response.status_code, 200)

    def test_get_file_from_mongodb(self):
        response = self.client.get(
            'http://localhost:8000/webapp/api/products/collection/')
        self.assertEqual(response.status_code, 200)

    def test_get_collection_name(self):
        """
        get list collection product by distinct method mongoengine
        """
        response = self.client.get(
            'http://localhost:8000/webapp/api/products/collection/')
        self.assertEqual(response.status_code, 200)
