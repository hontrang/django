import ast
import os
import time
import logging

from django.core import serializers


from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from PIL import Image
from django.utils.six import BytesIO
from rest_framework import status
from rest_framework.decorators import api_view, detail_route, list_route
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from .utils import FileHandle
from .models import Products, Users
from .pagination import *
from .serializers import ProductSerializer, UserSerializer

logger = logging.getLogger(__name__)


class BaseViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    """
    Create a model instance.
    """

    def initialize_request(self, request, *args, **kwargs):
        """
        Set the `.action` attribute on the view,
        depending on the request method.
        """
        request = super(BaseViewSet, self).initialize_request(request, *args, **kwargs)
        # logger.debug(type(request))
        # logger.debug(request.data.getlist('cartList',None))
        return request


class ProductViewSet(BaseViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    @list_route(methods=['GET'])
    def collection(self, request, *args, **kwargs):
        """
        Test distinct in mongoengine, this feature is used to get category name
        """
        snippets = Products.objects.distinct('collection.collectionName')
        return Response(snippets, status=status.HTTP_200_OK)

    @detail_route(methods=['GET'])
    def image(self, request, id=None, *args, **kwargs):
        snippets = Products.objects.get(id=id)
        ch = snippets['imageSource'].readchunk()
        stream = BytesIO(ch)
        img = Image.open(stream)
        response = HttpResponse(ch, content_type=img.format)
        response['Content-Disposition'] = "filename=%s.%s" % (id, img.format)
        return response

    @detail_route(methods=['GET'])
    def limit(self, request, max=10, *args, **kwargs):
        snippets = Products.objects[:int(max)]
        serializer = ProductSerializer(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['GET'])
    def top_view(self, request, *args, **kwargs):
        """
        Method to get top viewed product, size = 10 products
        """
        if request.method == 'GET':
            snippets = Products.objects[:int(10)].order_by('-views')
            serializer = ProductSerializer(snippets, many=True)
            return Response(serializer.data)

    @list_route(methods=['GET'])
    def top_favorite(self, request, *args, **kwargs):
        """
        Method to get top viewed product, size = 10 products
        """
        snippets = Products.objects[:int(10)].order_by('-favorite')
        serializer = ProductSerializer(snippets, many=True)
        return Response(serializer.data)

    @list_route(methods=['GET'])
    def top_price(self, request, *args, **kwargs):
        """
        Method to get top viewed product, size = 10 products
        """
        snippets = Products.objects[:int(10)].order_by('-price')
        serializer = ProductSerializer(snippets, many=True)
        return Response(serializer.data)

    @list_route(methods=['GET'])
    def newest(self, request, *args, **kwargs):
        """
        Method to get top viewed product, size = 10 products
        """
        snippets = Products.objects[:int(10)].order_by('-created')
        serializer = ProductSerializer(snippets, many=True)
        return Response(serializer.data)

    @detail_route(methods=['PUT', 'POST'])
    def likeup(self, request, *args, **kwargs):
        """
        Method to add 1 to like
        """
        instance = self.get_object()
        _like = instance['like'] + 1
        snippets = Products.objects.get(id=instance['id']).update(like=_like)
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['PUT', 'POST'])
    def likedown(self, request, *args, **kwargs):
        """
        Method to minus 1 to like
        """
        instance = self.get_object()
        _like = instance['like'] - 1
        snippets = Products.objects.get(id=instance['id']).update(like=_like)
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['GET'])
    def price(self, request, id, *args, **kwargs):
        """
        Method to minus 1 to like
        """
        snippets = Products.objects.get(id=id)
        ch = snippets['price']
        return Response(ch, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def product_list(request):
    """
    List all product, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Products.objects.all()
        serializer = ProductSerializer(snippets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_image_from_id(request, id):
    """
    method to get file from Gridfs then return to client
    """
    snippets = Products.objects.get(id=id)
    ch = snippets['imageSource'].readchunk()
    return HttpResponse(ch, content_type="image/jpeg")


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def product_list_by_max(request, max, *args, **kwargs):
    """
    List product, limited by max
    """
    if request.method == 'GET':
        snippets = Products.objects[:int(max)]
        serializer = ProductSerializer(snippets, many=True)
        return Response(serializer.data)


class UserViewSet(BaseViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    @list_route(methods=['POST'])
    def login(self, request, *args, **kwargs):
        """
        Login user, check group of user, if pass return 200, else return 405
        """
        snippets = Users.objects.get(email=request.data['email'])
        serializer = UserSerializer(snippets)
        if (serializer.data['password'] == request.data['password']):
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['GET'])
    def group_user(self, *args, **kwargs):
        snippets = Users.objects.distinct('group')
        return Response(snippets, status=status.HTTP_200_OK)

    @detail_route(methods=['GET'])
    def image(self, request, id=None, *args, **kwargs):
        snippets = Users.objects.get(id=id)
        ch = snippets['avatar'].readchunk()
        stream = BytesIO(ch)
        img = Image.open(stream)
        response = HttpResponse(ch, content_type=img.format)
        response['Content-Disposition'] = "filename=%s.%s" % (id, img.format)
        return response

    @list_route(methods=['GET'])
    def collection(self, request, *args, **kwargs):
        """
        Test distinct in mongoengine, this feature is used to get group user name
        """
        snippets = Users.objects.distinct('group')
        return Response(snippets, status=status.HTTP_200_OK)

    @detail_route(methods=['GET'])
    def aggregate(self, request, id=None, *args, **kwargs):
        """
        Test distinct in mongoengine, this feature is used to get group user name
        """
        pipeline = {
            '$lookup':
            {
                'from': 'products',
                'localField': 'cartList',
                'foreignField': '_id',
                'as': 'product_in_cartList'
            }
        }
        snippets = Users.objects(id=id).aggregate(pipeline)
        return Response('', status=status.HTTP_200_OK)
