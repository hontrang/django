from django.db import models
from mongoengine import *
import datetime

class Product(Document):
    name = StringField(max_length=200)
    created = DateTimeField(default=datetime.datetime.now,auto_now_add=True)
    imageUrl = StringField(max_length=200)

class User(Document):
    username = StringField(max_length=100, min_length=None, allow_blank=False, trim_whitespace=True)
    password = StringField(style={'input_type': 'password'},max_length=50, min_length=4, allow_blank=False, trim_whitespace=True)
    email = EmailField(domain_whitelist=None, allow_utf8_user=False, allow_ip_domain=False)
    created = DateTimeField(default=datetime.datetime.now,auto_now_add=True)
# Create your models here.
