from django.contrib import admin

from apps.core.models import Item, \
    Occupation, \
    Order, \
    Restaurant, \
    RestaurantUser, \
    Table

admin.site.register(Item)
admin.site.register(Occupation)
admin.site.register(Order)
admin.site.register(Restaurant)
admin.site.register(RestaurantUser)
admin.site.register(Table)