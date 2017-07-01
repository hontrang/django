"""
declare serializers
"""
import time
from django.conf import settings
from rest_framework_mongoengine import serializers
from .models import Products, Users, Collection

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

