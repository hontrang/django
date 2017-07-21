"""
declare serializers
"""
import logging
from django.conf import settings
from rest_framework_mongoengine import serializers
from .models import *
from mongoengine.errors import ValidationError as me_ValidationError

logger = logging.getLogger(__name__)


def raise_errors_on_nested_writes(method_name, serializer, validated_data):
    # *** inherited from DRF 3, altered for EmbeddedDocumentSerializer to pass ***
    assert not any(
        isinstance(field, serializers.DocumentSerializer) and
        not isinstance(field, serializers.EmbeddedDocumentSerializer) and
        (key in validated_data)
        for key, field in serializer.fields.items()
    ), (
        'The `.{method_name}()` method does not support writable nested'
        'fields by default.\nWrite an explicit `.{method_name}()` method for '
        'serializer `{module}.{class_name}`, or set `read_only=True` on '
        'nested serializer fields.'.format(
            method_name=method_name,
            module=serializer.__class__.__module__,
            class_name=serializer.__class__.__name__
        )
    )

    assert not any(
        '.' in field.source and (key in validated_data) and
        isinstance(validated_data[key], (list, dict))
        for key, field in serializer.fields.items()
    ), (
        'The `.{method_name}()` method does not support writable dotted-source '
        'fields by default.\nWrite an explicit `.{method_name}()` method for '
        'serializer `{module}.{class_name}`, or set `read_only=True` on '
        'dotted-source serializer fields.'.format(
            method_name=method_name,
            module=serializer.__class__.__module__,
            class_name=serializer.__class__.__name__
        )
    )


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
    # cartList = ProductSerializer(many=True, read_only=True)

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

