from django.conf.urls import url, include
from rest_framework import routers
from webappsql import views



router = routers.DefaultRouter()
router.register(r'customer', views.CustomerViewSet)
router.register(r'deliveryinfo', views.DeliveryInfoViewSet)
router.register(r'payment', views.PaymentViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'collection', views.CollectionViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]