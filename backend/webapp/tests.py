"""
declare simple testcase, only http test still now
"""
# import os
from django.test import TestCase
from django.test import Client
# Create your tests here.


class HttpServiceTestCase(TestCase):
    """
    Testcases to validate http service usage
    """

    def setUp(self):
        """
        Setting up testcases
        """
        print('=========== ROOT DIR ============')
        # show list items in directory
        # print(os.listdir())
        self.client = Client()

        response = self.client.get('http://localhost:8000/upload_file/upload')
        self.assertEqual(response.status_code, 200)

    def test_post_a_file_to_http(self):
        """
        http upload file to api, file is located ".static"
        """
        with open('./client_assets/dog.jpg', 'rb') as file:
            response = self.client.post('http://localhost:8000/upload_file/upload', {
                                        'title': 'test post', 'imageUrl': file}, format='multipart')
        self.assertEqual(response.status_code, 200)

    
    def test_upload_file_product(self):
        """
        test http post file product serializer
        """
        with open('./client_assets/dog.jpg', 'rb') as file:
            response = self.client.post('http://localhost:8000/api-authenticated/products/', {
                                        'title': 'test post', 'imageUrl': file}, format='multipart')
        print(response)
        self.assertEqual(response.status_code, 201)
