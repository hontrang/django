import datetime
import logging
import os
from django import forms
from django.db import models

from django.db.models.signals import pre_delete, pre_save, post_save, post_delete
from django.dispatch.dispatcher import receiver

logger = logging.getLogger(__name__)


# Create your models here.
class User(models.Model):
    """
    Model for entire users ex:customer, administrator, moderator ...
    """
    name = models.CharField(max_length=100, default="To be updated")
    email = models.EmailField(max_length=100,default="To be updated")
    birdthday = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=20)
    firstName = models.CharField(max_length=100,default="To be updated")
    lastName = models.CharField(max_length=100,default="To be updated")
    avatar = models.ImageField(max_length=100, default="To be updated", upload_to="storage")
    deliveryAddress = models.ForeignKey('DeliveryInfo',null=True,related_name='deliveryinfo')
    # payment = models.ForeignKey('Payment',null=True,related_name='user_payment')
    returnItems= models.ManyToManyField('Product', blank=True,related_name='returnitems')
    cartList = models.ManyToManyField('Product', blank=True, related_name='cartlist')
    favorite = models.ManyToManyField('Product', blank=True, related_name='favorite')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    level = models.IntegerField(default=0)
    group = models.CharField(max_length=100,default="customer")

    def __str__(self):
        return f'{self.pk} - {self.name} - {self.email}'


class DeliveryInfo(models.Model):
    name = models.CharField(max_length=100, default='To be updated')
    phoneNumber = models.CharField(max_length=20, default="To be updated")
    homeAddress = models.TextField(max_length=500, default='To be updated')
    province = models.TextField(max_length=500, default='To be updated')
    district = models.TextField(max_length=500, default='To be updated')
    area = models.TextField(max_length=500, default='To be updated')
    def __str__(self):
        return f'{self.pk} - {self.name}'

class Payment(models.Model):
    cardBrand = models.CharField(max_length=100, default='To be updated')
    expirationDate = models.DateTimeField(auto_now_add=True)
    cardNumber = models.CharField(max_length=100, default='To be updated')
    relatedUser = models.ForeignKey('User', null=True, related_name='payment')
    def __str__(self):
        return f'{self.pk} - {self.cardBrand} - {self.cardNumber[5:]}'


class Product(models.Model):
    """
    model for product
    """ 
    title = models.CharField(max_length=100, default='To be updated')
    collection = models.ForeignKey('Collection',null=True)
    simpleDesc = models.TextField(max_length=500, default='To be updated')
    fullDesc = models.TextField(max_length=500, default='To be updated')
    price = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    imageSource = models.ImageField(max_length=100, default="To be updated", upload_to="storage")
    discount = models.CharField(max_length=100, default='To be updated')
    
    def __str__(self):
        return f'{self.pk} - {self.title}'

class Collection(models.Model):
    collectionName = models.CharField(max_length=100 ,default="To be updated")
    collectionDesc = models.TextField(max_length=500 ,default="To be updated")
    created = models.DateTimeField(auto_now_add=True, null=True)
    author = models.ManyToManyField('User', blank=True)

    def __str__(self):
        return f'{self.pk} - {self.collectionName}'
# refer https://docs.djangoproject.com/en/1.11/topics/signals/
@receiver(post_delete, sender=Product)
def product_post_delete_signal(sender, instance, using,**kwargs):
    if instance.imageSource:
        if os.path.isfile(instance.imageSource.path):
            instance.imageSource.delete(save=False)

@receiver(pre_save, sender=Product)
def product_pre_save_signal(sender, instance, raw, using, update_fields, **kwargs):
    if instance.pk:
        oldInstance = sender.objects.get(id=instance.pk)
        if os.path.isfile(oldInstance.imageSource.path):
            oldInstance.imageSource.delete(save=False)

@receiver(post_delete, sender=User)
def user_post_delete_signal(sender, instance, using, **kwargs):
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            instance.avatar.delete(save=False)

@receiver(pre_save, sender=User)
def user_pre_save_signal(sender, instance, raw, using, update_fields, **kwargs):
    if instance.pk:
        oldAvatar = sender.objects.get(id=instance.pk)
        if os.path.isfile(oldAvatar.avatar.path):
            oldAvatar.avatar.delete(save=False)

@receiver(post_save, sender=User)
def user_post_save_signal(sender, instance, using, **kwargs):
    pass