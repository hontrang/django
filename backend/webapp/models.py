"""
declare models
"""
import datetime
from django.db import models
from mongoengine import *


class Products(Document):
    """
    model for product
    """
    title = StringField(max_length=200,required=True)
    cateID = StringField(max_length=100)
    simpleDesc = StringField(max_length=200)
    fullDesc = StringField(max_length=500)
    price = IntField()
    views = IntField()
    favorite = IntField()
    created = DateTimeField(default=datetime.datetime.now,auto_now_add=True)
    imageSource = ImageField(size=None,thumbnail_size=None, collection_name='images');
    imageUrl = StringField(max_length=200,required=False)
    discount = StringField(max_length=200)

class Users(Document):
    """
    model for user
    """
    username = StringField(max_length=100, min_length=None, allow_blank=False, trim_hitespace=True,required=True)
    password = StringField(input_type='password',max_length=50, min_length=8, allow_blank=False, trim_whitespace=True,required=True)
    displayname = StringField(max_length=100, min_length=None, allow_blank=False, trim_whitespace=True, default="None")
    firstName = StringField(max_length=100, min_length=None, allow_blank=False, trim_whitespace=True, default="None")
    lastname = StringField(max_length=100, min_length=None, allow_blank=False, trim_whitespace=True, default="None")
    avatar = ImageField(size=None,thumbnail_size=None, collection_name='images');
    email = EmailField(domain_whitelist=None, allow_utf8_user=False, allow_ip_domain=False,required=True)
    created = DateTimeField(default=datetime.datetime.now,auto_now_add=True)
    level = IntField(min_value=1, max_value=5, default = 1)
# Create your models here.
