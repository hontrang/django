from rest_framework_mongoengine import serializers
from .models import *
class  ProductSerializer(serializers.DocumentSerializer):
    # image= serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        model = Products
        fields = ('id','title','created','imageUrl')

class  UserSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Users
        fields = ('id','username','password','displayname','firstName','lastname','avatar','email','created','level')