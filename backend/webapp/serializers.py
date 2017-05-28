from rest_framework_mongoengine import serializers
from .models import *
class  ProductSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Product
        fields = ('id','name','imageUrl')

class  UserSerializer(serializers.DocumentSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','email')