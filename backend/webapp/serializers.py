"""
declare serializers
"""
import logging
from django.conf import settings
from rest_framework_mongoengine import serializers
from .models import *
from mongoengine.errors import ValidationError as me_ValidationError

logger = logging.getLogger(__name__)


class BaseAppSerializer(serializers.DocumentSerializer):
    """define base serializer
    """
    class Meta:
        pass

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)

        instance = self.recursive_save(validated_data, instance)
        logger.debug(instance)
        return instance


class CollectionSerializer(serializers.EmbeddedDocumentSerializer):
    """
    Embedded Field for Products
    """
    class Meta:
        model = Collection
        fields = '__all__'


class ProductSerializer(BaseAppSerializer):
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


class UserSerializer(BaseAppSerializer):
    """
    TBD
    """
    deliveryAddress = DeliveryInfoSerializer(many=True, read_only=True)
    payment = PaymentSerializer(many=True, read_only=True)

    class Meta:
        """
        TBD
        """
        model = Users
        fields = '__all__'
        ordering = ['-created']
        # depth = 2
    
    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        logger.debug(validated_data)
        instance = self.recursive_save(validated_data, instance)

        return instance

