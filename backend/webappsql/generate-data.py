from requests_toolbelt import MultipartEncoder
import requests
from random import randint
import logging
import unittest
import uuid
from utils import randomNumber

logger = logging.getLogger(__name__)


def generateProduct():
    for index in range(1, 100):
        rand = randint(1, 100)
        file = open('../client_assets/dog.jpg', 'rb')
        product = {
            'title': f'san pham {rand}',
            'simpleDesc': f'san pham desc {rand}',
            'fullDesc': f'san pham full desc {rand}',
            'price': f'{rand}',
            'like': f'{rand}',
            'imageSource': (file.name, file),
            'discount': f'san pham sale {rand}'
        }
        # print(product)
        encoder = MultipartEncoder(product)
        # print(encoder.to_string())
        r0 = requests.post('http://localhost:8000/webapp2/api/product/',
                           data=encoder, headers={'Content-Type': encoder.content_type})
        print(r0.json())
        assert r0.status_code == 201

def generateCollection():
    lt = ['Apple', 'Samsung', 'Nokia', 'Blackberry', 'LG', 'Xiaomi', 'Oppo', 'Lenovo']
    for index in lt:
        rand = randint(1, 100)
        file = open('../client_assets/dog.jpg', 'rb')
        
        collection = {
            'collectionName': index,
            'collectionDesc': 'San pham cua %s' %index
        }
        # print(product)
        encoder = MultipartEncoder(collection)
        # print(encoder.to_string())
        r0 = requests.post('http://localhost:8000/webapp2/api/collection/',
                           data=encoder, headers={'Content-Type': encoder.content_type})
        print(r0.json())
        assert r0.status_code == 201


def generatePayment():
    for i in range(10):
        rand = randint(0,9)
        payment = {
            'cardBrand': 'the tin dung ngan hang %d' % rand,
            'cardNumber': randomNumber(12)
        }
        encoder = MultipartEncoder(payment)
        r0 = requests.post('http://localhost:8000/webapp2/api/payment/',
                           data=encoder, headers={'Content-Type': encoder.content_type})
        print(r0.json())
        assert r0.status_code == 201

def generateDeliveryInfo():
    for i in range(10):
        rand = randint(1,10)
        deliveryinfo = {
            'name': 'Ten dia chi giao hang %d' % rand,
            'phoneNumber': randomNumber(12),
            'homeAddress': 'dia chi nha %d' %rand,
            'province': 'Thanh pho Ho Chi Minh',
            'district': 'Quan %d' %rand,
            'area': 'Khu vuc %d' %rand
        }
        encoder = MultipartEncoder(deliveryinfo)
        r0 = requests.post('http://localhost:8000/webapp2/api/deliveryinfo/',
                           data=encoder, headers={'Content-Type': encoder.content_type})
        print(r0.json())
        assert r0.status_code == 201
        
def generateCustomer():
    for i in range(100):
        file = open('../client_assets/index.jpg', 'rb')
        rand = randint(1,10)
        customer = {
          'name': 'khach hang %d' %rand,
          'email': 'khachhang%d@email.com' %rand,
          'password': '123456789',
          'firstName': 'khach',
          'lastName': 'hang %d' %rand,
          'avatar': (file.name,file),
          'level': '%d' %1,
          'group':  'cust',
        }
        encoder = MultipartEncoder(customer)
        r0 = requests.post('http://localhost:8000/webapp2/api/customer/',
                           data=encoder, headers={'Content-Type': encoder.content_type})
        print(r0.json())
        assert r0.status_code == 201



if __name__ == '__main__':
    # generateProduct()
    # generateCollection()
    # generatePayment()
    # generateDeliveryInfo()
    generateCustomer()

