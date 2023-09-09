from django.db import models
from accounts.models import User
from store.models import Product, Variation


class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.payment_id
    


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancellation', 'Cancellation')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    is_ordered = models.BooleanField(default=False)
    tax = models.FloatField()
    status = models.CharField(max_length=30, choices=STATUS, default='New')
    ip = models.CharField(max_length=20, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def full_name(self):
        return self.first_name + " "+ self.last_name
    
    def full_address(self):
        return f'{self.address_line_1 + " "+ self.address_line_2}'

    def __str__(self):
        return self.first_name
    



class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation  = models.ForeignKey(Variation, on_delete=models.CASCADE)
    color = models.CharField(max_length=30)
    size = models.CharField(max_length=30)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.product.product_name

