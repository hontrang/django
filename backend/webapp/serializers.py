"""
declare serializers
"""
import time
from django.conf import settings
from rest_framework_mongoengine import serializers
from .models import Products, Users



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
        fields = ('id', 'username', 'password', 'displayname',
                  'firstName', 'lastname', 'avatar', 'email', 'created', 'level')

