"""
declare serializers
"""
import time
import logging
import ast
from django.conf import settings
from rest_framework_mongoengine import serializers
from rest_framework.exceptions import ValidationError
from .models import Products, Users, Collection
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



class UserSerializer(serializers.DocumentSerializer):
    """
    TBD
    """
    class Meta:
        """
        TBD
        """
        model = Users
        fields = '__all__'
        ordering = ['-created']

