"""
declare serializers
"""
import time
import logging
import ast
from django.conf import settings
from rest_framework_mongoengine import serializers
from rest_framework.exceptions import ValidationError
from .models import *
logger = logging.getLogger(__name__)

class CollectionSerializer(serializers.EmbeddedDocumentSerializer):
    """
    Embedded Field for Products
    """
    class Meta:
        model = Collection
        fields = '__all__'
        
class ProductSerializer(serializers.DocumentSerializer):
    """
    TBD
    """    
    class Meta:
        """
        TBD
        """
        model = Products
        fields = '__all__'
        ordering = ['-created']

class DeliveryInfoSerializer(serializers.EmbeddedDocumentSerializer):
    """
    define serializer for delivery info embedded document
    """
    class Meta:
        """
        TDB
        """
        model = DeliveryInfo
        fields = '__all__'

class PaymentSerializer(serializers.EmbeddedDocumentSerializer):
    """
    Define serializer for payment embedded document
    """
    class Meta:
        model = Payment
        fields = '__all__'

class UserSerializer(serializers.DocumentSerializer):
    """
    TBD
    """
    deliveryAddress = DeliveryInfoSerializer(many=True,read_only=True)
    payment = PaymentSerializer(many=True,read_only=True)
    returnItems = ProductSerializer(many=True,read_only=True)
    class Meta:
        """
        TBD
        """
        model = Users
        fields = '__all__'
        ordering = ['-created']
        depth = 2

