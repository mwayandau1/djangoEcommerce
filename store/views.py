from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def store(request, category_slug=None):
    categories = None
    products = None
    
    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().order_by('id')
    
    paginator = Paginator(products, 15)  # Initialize the paginator after the products are set
    
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)  # Use the paginator to paginate the products
    
    product_count = paged_products.paginator.count  # Use paged_products.paginator.count for the total count
    
    context = {
        'product_count': product_count,
        'products': paged_products,
    }
    return render(request, 'store/store.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-date_created').filter(
                Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
    product_count = products.count()
    context = {'products':products, 'product_count':product_count}
    return render(request, 'store/store.html', context)


def product_detail(request, product_slug, category_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product=product).exists()
        
    except Exception as e:
        raise e
    context = {'product':product, 'in_cart': in_cart}
    return render(request, 'store/product_detail.html', context)