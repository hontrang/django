from django.contrib import admin

# Register your models here.
from webappsql.models import Customer, Product, DeliveryInfo, Payment, Collection

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name','email','firstName', 'lastName','created','modified','avatar')

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product)
admin.site.register(DeliveryInfo)
admin.site.register(Payment)
admin.site.register(Collection)