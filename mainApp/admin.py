from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register((mainCategory,
                     Brand,
                     Product,
                     Profile,
                     Pics,
                     Wishlist,
                     Checkout,
                     Subscribers,
                     ContactUS))
