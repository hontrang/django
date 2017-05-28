from django.db import models
from mongoengine import *
import datetime

class Product(Document):
    name = StringField(max_length=200)
    created = DateTimeField(default=datetime.datetime.now)
    imageUrl = StringField(max_length=200)
# Create your models here.
