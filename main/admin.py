from django.contrib import admin
from .models import Food, Restaurant, Menu, Customer, Order


class CustomOrder(admin.ModelAdmin):
    filter_horizontal = ('product', 'product',)


admin.site.register(Food)
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Customer)
admin.site.register(Order, CustomOrder)


