from django.contrib import admin

# Register your models here.
from webappsql.models import User, Product, DeliveryInfo, Payment, Collection

admin.site.register(User)
admin.site.register(Product)
admin.site.register(DeliveryInfo)
admin.site.register(Payment)
admin.site.register(Collection)