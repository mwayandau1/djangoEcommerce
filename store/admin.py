from django.contrib import admin
from .models import Product, Variation, ReviewRating

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}

    list_display = ['product_name', 'category', 'is_available',  'stock', 'price', 'date_modified',]
    list_display_links = ['product_name']


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value',)


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'subject', 'rating']

admin.site.register(Product, ProductAdmin)

admin.site.register(Variation, VariationAdmin)

admin.site.register(ReviewRating, ReviewRatingAdmin)