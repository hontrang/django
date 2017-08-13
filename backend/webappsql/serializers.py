from rest_framework import serializers
from webappsql.models import User, DeliveryInfo, Payment, Product, Collection


class DeliveryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryInfo
        fields = '__all__'
        depth=2


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        depth=2


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth=2


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'
        depth=2

class UserSerializer(serializers.ModelSerializer):
    # cartList = ProductsSerializer(many=True)
    class Meta:
        model = User
        fields = '__all__'
        depth=2