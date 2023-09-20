from django.db import models
from category.models import Category
from accounts.models import User
from django.urls import reverse
from django.db.models import Avg, Count


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=400, blank=True)
    product_image = models.ImageField(upload_to='photos/product')
    price = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product_name

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def averageRating(self):
        review = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if review['average'] is not None:
            avg = float(review['average'])
        return avg
    def ratingCount(self):
        review = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        rating_count = 0
        if review['count'] is not None:
            rating_count = int(review['count'])
        return rating_count


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def size(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


class Variation(models.Model):
    variation_category_choices = (('color', 'color'), ('size', 'size'),)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choices)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self) -> str:
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    ip = models.CharField(max_length=30, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/product/', max_length=255)
    class Meta:
        verbose_name='ProductGallery'
        verbose_name_plural = 'Product Gallery'


    def __str__(self) -> str:
        return self.product.product_name