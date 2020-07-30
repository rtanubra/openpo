from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Basket)
admin.site.register(Location)