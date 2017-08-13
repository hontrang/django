from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponse
from webappsql.models import User, DeliveryInfo, Payment, Product, Collection
from webappsql.serializers import UserSerializer, DeliveryInfoSerializer, PaymentSerializer, ProductSerializer, CollectionSerializer
from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound
from django.core.urlresolvers import reverse
import datetime

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DeliveryInfoViewSet(viewsets.ModelViewSet):
    queryset = DeliveryInfo.objects.all()
    serializer_class = DeliveryInfoSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

