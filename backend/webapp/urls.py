from django.conf.urls import include, url
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from webapp import views


schema_view = get_swagger_view(title='Django REST API')


# this is DRF router for REST API viewsets
router = routers.DefaultRouter()


# register REST API endpoints with DRF router
router.register(r'products', views.ProductViewSet , r"products")
router.register(r'users', views.UserViewSet , r"users")

app_name = 'upload'
urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),#ex:
    url(r'^api/max/(?P<pk>[0-9]+)$', views.product_list_by_max),#ex:
    url(r'^api/collection/$', views.get_product_collection),#ex:
    url(r'^docs/', schema_view),#ex:
]