import os

from rest_framework_mongoengine import viewsets
from .models import Products, Users
from .utils import FileHandle
from .serializers import ProductSerializer, UserSerializer
from PIL import Image
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse
from rest_framework.parsers import JSONParser


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        request.data['imageUrl'] = FileHandle.saveFileLocal(
            self, request.data['imageSource'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Update a model instance.
        """
        request.data['imageUrl'] = FileHandle.saveFileLocal(
            self, request.data['imageSource'])
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        FileHandle.deleteExistedLocal(self,instance['imageUrl'])
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        FileHandle.deleteExistedLocal(self,instance['imageUrl'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'


@api_view(['GET', 'POST'])
def product_list(request):
    """
    List all product, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Products.objects.all()
        serializer = ProductSerializer(snippets, many=True)
        print(JsonResponse(serializer.data, safe=False))
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            data=serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_product_collection(request):
    """
    Test distinct in mongoengine, this feature is used to get category name
    """
    if request.method =='GET':
        snippets = Products.objects.distinct('title')
        print(JsonResponse(snippets, safe=False))
        return Response(snippets, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def product_list_by_max(request, pk):
    """
    List product, limited by max
    """
    if request.method == 'GET':
        snippets = Products.objects[:int(pk)]
        serializer = ProductSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
