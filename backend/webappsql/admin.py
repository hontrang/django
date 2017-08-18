from django.contrib import admin

# Register your models here.
from webappsql.models import User, Product, DeliveryInfo, Payment, Collection

class UserAdmin(admin.ModelAdmin):
    list_display = ('name','email','firstName', 'lastName','created','modified','avatar')

admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(DeliveryInfo)
admin.site.register(Payment)
admin.site.register(Collection)