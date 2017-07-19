"""
declare models
"""
import datetime

from django.db import models
from mongoengine import *


class Collection(EmbeddedDocument):
    """
    included collection info of products
    """
    collectionName = StringField(max_length=100)
    collectionDesc = StringField(max_length=100)


class Products(Document):
    """
    model for product
    """
    title = StringField(max_length=200, required=True)
    collection = EmbeddedDocumentListField(Collection)
    simpleDesc = StringField(max_length=200, default="To be updated")
    fullDesc = StringField(max_length=500, default="To be updated")
    price = IntField(default=0)
    views = IntField(default=0)
    like = IntField(default=0)
    created = DateTimeField(default=datetime.datetime.now, auto_now_add=True)
    imageSource = ImageField(
        size=None, thumbnail_size=None, collection_name='images')
    # imageUrl = StringField(max_length=200,required=False)
    discount = StringField(max_length=200)


class DeliveryInfo(EmbeddedDocument):
    """
    Delivery info set by customer to, that is customer contatc infomations
    """
    name = StringField(max_length=100, min_length=None,
                       allow_blank=False, trim_whitespace=True)
    phoneNumber = StringField(
        max_length=20, min_length=None, allow_blank=False, trim_whitespace=True)
    homeAddress = StringField(max_length=200, min_length=None)
    province = StringField(max_length=100, min_length=None)
    district = StringField(max_length=100, min_length=None)
    area = StringField(max_length=100, min_length=None)


class Payment(EmbeddedDocument):
    """
    Payment set by customer or record by customer history trading
    """
    cardBrand = StringField(max_length=50, min_length=None)
    expirationDate = DateTimeField()
    cardNumber = StringField(max_length=50, min_length=None)


class Users(Document):
    """
    model for user
    """
    name = StringField(max_length=100, min_length=None,
                       allow_blank=False, trim_whitespace=True)
    email = EmailField(domain_whitelist=None, allow_utf8_user=False,
                       allow_ip_domain=False, required=True)
    birdthday = DateTimeField(auto_now_add=True,default=datetime.datetime.now)
    password = StringField(input_type='password', max_length=50, min_length=8,
                           allow_blank=False, trim_whitespace=True, required=True)
    displayName = StringField(max_length=100, min_length=None,
                              allow_blank=False, trim_whitespace=True, default="To be updated")
    firstName = StringField(max_length=100, min_length=None,
                            allow_blank=False, trim_whitespace=True, default="To be updated")
    lastName = StringField(max_length=100, min_length=None,
                           allow_blank=False, trim_whitespace=True, default="To be updated")
    avatar = ImageField(size=None, thumbnail_size=None,
                        collection_name='images')
    deliveryAddress = EmbeddedDocumentListField(DeliveryInfo)
    payment = EmbeddedDocumentListField(Payment)
    returnItems=ReferenceField(Products,reverse_delete_rule=CASCADE)
    cartList = ReferenceField(Products,reverse_delete_rule=CASCADE)
    favorite = ReferenceField(Products,reverse_delete_rule=CASCADE)
    created = DateTimeField(default=datetime.datetime.now, auto_now_add=True)
    level = IntField(min_value=1, max_value=5, default=1)
    group = StringField(default='customer',
                        allow_blank=False, trim_whitespace=True)
    # group = ListField(StringField(), default=["customer","admin","provider"])
# Create your models here.
