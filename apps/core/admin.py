from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.core.models import Item, \
    ItemImage, \
    Occupation, \
    Order, \
    Restaurant, \
    RestaurantUser, \
    Table


class CustomUserAdmin(UserAdmin):
    model = RestaurantUser
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'restaurant', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('restaurant',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('restaurant',)}),
    )


admin.site.register(Item)
admin.site.register(ItemImage)
admin.site.register(Occupation)
admin.site.register(Order)
admin.site.register(Restaurant)
admin.site.register(RestaurantUser, CustomUserAdmin)
admin.site.register(Table)
