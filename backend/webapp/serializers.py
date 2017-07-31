"""
declare serializers
"""
import logging
import copy
import ast
import inspect
from django.conf import settings
from mongoengine.errors import ValidationError as me_ValidationError
from rest_framework_mongoengine import serializers
from rest_framework import serializers as drf
from collections import Mapping, OrderedDict

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.settings import api_settings
from rest_framework.fields import set_value
from rest_framework.fields import (  # NOQA # isort:skip
    CreateOnlyDefault, CurrentUserDefault, SkipField, empty
)

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
    deliveryAddress = DeliveryInfoSerializer(many=True, read_only=True)
    payment = PaymentSerializer(many=True, read_only=True)
    # cartList = ListReference()

    class Meta:
        """
        TBD
        """
        model = Users
        fields = '__all__'
        ordering = ['-created']
        depth = 2

    def to_internal_value(self, data):
        """
        Calls super() from DRF, but with an addition.
        Creates initial_data and _validated_data for nested
        EmbeddedDocumentSerializers, so that recursive_save could make
        use of them.
        If meets any arbitrary data, not expected by fields,
        just silently drops them from validated_data.
        """
        # for EmbeddedDocumentSerializers create initial data
        # so that _get_dynamic_data could use them
        for field in self._writable_fields:
            if isinstance(field, serializers.EmbeddedDocumentSerializer) and field.field_name in data:
                field.initial_data = data[field.field_name]
            if isinstance(field, drf.ListField) and field.field_name in data and hasattr(field, 'child'):
                child_data = field.get_value(data)
                li=[]
                for x in  range((len(child_data))):
                    j = ast.literal_eval(child_data[x])                    
                    d = field.child.get_value(ast.literal_eval(child_data[x]))
                    query = Products.objects.get(id=j['_id'])
                    li.append(query)
                    
        ret = super(serializers.DocumentSerializer, self).to_internal_value(data)
        # for EmbeddedDocumentSerializers create _validated_data
        # so that create()/update() could use them
        for field in self._writable_fields:
            logger.debug(field.field_name)
            if isinstance(field, serializers.EmbeddedDocumentSerializer) and field.field_name in ret:
                field._validated_data = ret[field.field_name]
            if isinstance(field, drf.ListField) and field.field_name in data and hasattr(field, 'child'):
                ret[field.field_name] = li
        return ret


