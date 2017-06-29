"""
declare serializers
"""

from rest_framework_mongoengine import serializers
from .models import Products, Users


class ProductSerializer(serializers.DocumentSerializer):
    """
    TBD
    """
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        # print('++++++++++++++++++++++++++++++++++++')
        # print(validated_data)
        return Products.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.created = validated_data.get('created', instance.created)
        instance.imageUrl = validated_data.get('imageUrl', instance.imageUrl)
        instance.save()
        return instance
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

