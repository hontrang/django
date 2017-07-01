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
        # print('=========== ROOT DIR ============')
        # show list items in directory
        # print(os.listdir())
        self.client = Client()

    # def test_post_a_file_to_http(self):
    #     """
    #     http upload file to api, file is located ".static"
    #     """
    #     with open('./client_assets/dog.jpg', 'rb') as file:
    #         response = self.client.post('http://localhost:8000/upload_file/upload', {
    #                                     'title': 'test post', 'imageSource': file}, format='multipart')
    #     self.assertEqual(response.status_code, 200)

    
    def test_upload_file_product(self):
        """
        test http post file product serializer
        """
        with open('./client_assets/dog.jpg', 'rb') as file:
            response = self.client.post('http://localhost:8000/webapp/api/products/', {
                                        'title': 'test post', 'imageSource': file}, format='multipart')
        imageSourceID = response.data['imageSource']
        self.assertEqual(response.status_code, 201)
        with open('./client_assets/index.jpg', 'rb') as file:
            response = self.client.delete('http://localhost:8000/webapp/api/products/%s/' % imageSourceID)
            print(response.data)
            self.assertEqual(response.status_code, 201)

    def test_upload_100_products(self):
        """
        test to upload 100 products in a short time
        """
        for index in range(1,100):
            with open('./client_assets/dog.jpg', 'rb') as file:
                response = self.client.post('http://localhost:8000/webapp/api/products/', {
                                            'title': 'test post 1', 'imageSource': file}, format='multipart')
            self.assertEqual(response.status_code, 201)
    # def test_get_list_all_product(self):
    #     response = self.client.get('http://localhost:8000/webapp/api/products/')
    #     self.assertEqual(response.status_code, 200)

    # def test_get_file_product_by_id(self):
    #     response = self.client.get('http://localhost:8000/webapp/api/products/5954af0396279a1d6cb12264/')
    #     self.assertEqual(response.status_code, 200)

    # def test_update_file_product(self):
    #     """
    #     test http put to update imageSource field in product
    #     """
    #     with open('./client_assets/index.jpg', 'rb') as file:
    #         response = self.client.put('http://localhost:8000/webapp/api/products/5954af0396279a1d6cb12264/', {
    #                                     'title': 'test post', 'imageSource': file}, format='multipart')
        # self.assertEqual(response.status_code, 201)

    # def test_get_file_from_mongodb(self):
    #     pass
        
