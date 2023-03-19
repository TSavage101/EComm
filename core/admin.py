from django.contrib import admin

from .models import Product, Rating, Number, Feedback, Cart, Cart_item

# Register your models here.
admin.site.register(Product)

admin.site.register(Rating)

admin.site.register(Number)

admin.site.register(Feedback)

admin.site.register(Cart)

admin.site.register(Cart_item)