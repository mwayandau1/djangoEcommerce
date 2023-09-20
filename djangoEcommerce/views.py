from django.shortcuts import render
from store.models import Product, ReviewRating
from django.core.paginator import Paginator
def home(request):
    products = Product.objects.all().filter(is_available = True).order_by('date_created')
    for product in products:
        review_rating = ReviewRating.objects.filter(product_id=product.id, status=True)
    
    context = {'products':products,
               'review_rating':review_rating}
    return render(request, 'home.html', context)