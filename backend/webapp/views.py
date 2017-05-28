from rest_framework_mongoengine import viewsets
from .models import *
from .serializers import *
from rest_framework import generics
# def index(request):
#     response = HttpResponse()
#     response.write("<h1>Welcome</h1>")
#     response.write("This is the polls app")
#     return response
#
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer