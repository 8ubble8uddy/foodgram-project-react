from django.contrib import admin

from apps.services.models import Favorite, ShoppingCart, Subscribe

admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.register(Subscribe)
