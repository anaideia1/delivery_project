from django.contrib import admin

from api.orders.models import Order


class OrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)
