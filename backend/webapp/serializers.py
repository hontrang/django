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
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        filesrc = validated_data['imageSource']
        validated_data['imageUrl'] = self.saveFileLocal(filesrc)
        return Products.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.created = validated_data.get('created', instance.created)
        instance.imageSource = validated_data.get('imageSource', instance.imageSource)
        instance.imageUrl = self.saveFileLocal(validated_data['imageSource'])
        instance.save()
        return instance
    def saveFileLocal(self, source):
        filesrc = source
        ch = filesrc.chunks()
        filename = "%s-%s" %(str(time.time()).replace('.','_'), filesrc.name)
        with open('%s/%s' %(settings.STATICFILES_DIRS, filename ), 'w+b') as file:
            for d in ch:
                file.write(d)
            file.close()
        return filename
    
    def deleteExistedLocal(self, source):
        pass

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

