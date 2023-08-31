from django.db import models
from store.models import Product, Variation

class Cart(models.Model):
    cart_id = models.CharField(max_length=200, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.cart_id
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_available = models.BooleanField(default=True)


    def __str__(self) -> str:
        return self.product.product_name
    

    def sub_total(self):
        return (self.quantity * self.product.price)
    