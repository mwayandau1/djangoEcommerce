from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}

    list_display = ['product_name', 'category', 'is_available',  'stock', 'price', 'date_modified',]
    list_display_links = ['product_name']

admin.site.register(Product, ProductAdmin)