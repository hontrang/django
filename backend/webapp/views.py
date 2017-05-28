from rest_framework_mongoengine import viewsets
from .models import *
from .serializers import *
# def index(request):
#     response = HttpResponse()
#     response.write("<h1>Welcome</h1>")
#     response.write("This is the polls app")
#     return response
#
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.create(name="name",imageUrl="imageUrl")
    serializer_class = ProductSerializer