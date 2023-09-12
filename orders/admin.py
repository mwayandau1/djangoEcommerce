from django.contrib import admin
from .models import Order, OrderProduct, Payment

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['payment', 'user', 'product', 'ordered', 'product_price', 'quantity', 'variations']
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name','phone', 'email','address_line_1', 'country', 'state',
                    'city', 'order_total', 'status', 'is_ordered']
    list_filter = ['status', 'is_ordered']
    list_display_links = ['order_number', 'phone', 'email', 'full_name']
    list_per_page = 20
    inlines = [OrderProductInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Payment)
