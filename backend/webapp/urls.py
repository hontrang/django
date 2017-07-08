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
    url(r'^api/max/(?P<max>[0-9]+)/$', views.product_list_by_max),#ex:
    url(r'^api/static-image/(?P<id>[^/.]+)/$', views.get_image_from_id),#ex:
    url(r'^docs/', schema_view),#ex:
]