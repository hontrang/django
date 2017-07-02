"""
declare simple testcase, only http test still now
"""
import json
from random import randint, randrange

# import os
from django.test import Client, TestCase


# Create your tests here.


class HttpServiceTestCase(TestCase):
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
                                        'title': 'test post', 'imageSource': file, 'collection': coll}, format='multipart')
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
                favorite = randint(0, 10000)
                price = randrange(10000, 1000000, 1000)
                response = self.client.post('http://localhost:8000/webapp/api/products/', {
                                            'title': 'test post 1', 'imageSource': file, 'collection': coll, 'views': views, 'favorite': favorite, 'price': price}, format='multipart')
            self.assertEqual(response.status_code, 201)

    def test_get_list_all_product(self):
        response = self.client.get(
            'http://localhost:8000/webapp/api/products/')
        self.assertEqual(response.status_code, 200)

    def test_get_file_from_mongodb(self):
        response = self.client.get(
            'http://localhost:8000/webapp/api/collection/')
        self.assertEqual(response.status_code, 200)

    def test_get_collection_name(self):
        """
        get list collection product by distinct method mongoengine
        """
        response = self.client.get(
            'http://localhost:8000/webapp/api/products/collection/')
        self.assertEqual(response.status_code, 200)
