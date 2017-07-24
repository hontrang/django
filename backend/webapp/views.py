import ast
import os
import time
import logging
from bson.json_util import dumps


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

from .models import Products, Users
from .pagination import *
from .serializers import ProductSerializer, UserSerializer
from .utils import FileHandle

logger = logging.getLogger(__name__)


class BaseViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    """
    Create a model instance.
    """


class ProductViewSet(BaseViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        # request.data['imageUrl'] = FileHandle.saveFileLocal(
        #     self, request.data['imageSource'])
        logger.debug(request.data)
        # if request.data['collection']:
        #     request.data['collection'] = ast.literal_eval(request.data['collection'])
        collection = request.data.get('collection')
        collection = self.convertStringToDict(collection)
        request.data['collection'] = collection
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Update a model instance.
        """
        # request.data['imageUrl'] = FileHandle.saveFileLocal(
        #     self, request.data['imageSource'])
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # FileHandle.deleteExistedLocal(self, instance['imageUrl'])
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

    def convertStringToDict(self, data):
        if type(data) is str:
            return ast.literal_eval(data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # FileHandle.deleteExistedLocal(self, instance['imageUrl'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(methods=['GET'])
    def collection(self, request, *args, **kwargs):
        """
        Test distinct in mongoengine, this feature is used to get category name
        """
        snippets = Products.objects.distinct('collection.collectionName')
        logger.debug(snippets)
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

    @detail_route(methods=['PUT'])
    def likeup(self, request, *args, **kwargs):
        """
        Method to add 1 to like
        """
        instance = self.get_object()
        _like = instance['like']
        _like += 1
        snippets = Products.objects.update(like=_like)
        return Response(status=status.HTTP_201_CREATED)

    @detail_route(methods=['PUT'])
    def likedown(self, request, *args, **kwargs):
        """
        Method to minus 1 to like
        """
        instance = self.get_object()
        _like = instance['like']
        _like -= 1
        snippets = Products.objects.update(like=_like)
        return Response(status=status.HTTP_201_CREATED)

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
        logger.debug(snippets)
        serializer = UserSerializer(snippets)
        logger.debug(serializer.data)
        if (serializer.data['password'] == request.data['password']):
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['GET'])
    def group_user(self, *args, **kwargs):
        snippets = Users.objects.distinct('group')
        logger.debug(snippets)
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
    def aggregate(self, request, id=None,*args, **kwargs):
        """
        Test distinct in mongoengine, this feature is used to get group user name
        """
        pipeline = {
            '$lookup':
            {
                'from':'products',
                'localField':'cartList',
                'foreignField':'_id',
                'as':'product_in_cartList'
            }
        }

        pipeline1 = {
            '$match':{
                'name':'user3082'
            }
        }
        snippets = list(Users.objects(id=id).aggregate(pipeline1))
        logger.debug(snippets)
        serializer = UserSerializer(snippets)
        logger.debug(serializer.data)

        return Response('',status=status.HTTP_200_OK)