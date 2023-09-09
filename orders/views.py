from django.shortcuts import render, redirect
from cart.models import CartItem, Cart
from .forms import OrdersForm
from .models import Order
import datetime
from django.http import HttpResponse

def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    order_total = 0
    tax = 0
    for cart_item in cart_items:
        order_total += (cart_item.product.price *cart_item.quantity)
        quantity = cart_item.quantity
        tax = order_total * (1/100)
        grand_total = order_total + tax
    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            #Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            data.order_number = current_date + str(data.id)
            data.save()
            order = Order.objects.get(user=current_user, is_ordered = False, order_number=data.order_number)
            context = {
                'order':order,
                'cart_items':cart_items,
                'total':order_total,
                'tax':tax,
                'grand_total':grand_total
            }
            return render(request, 'orders/payment.html', context)
        else:
            print(form.errors)
            return redirect('checkout')
   
def payment(request):

    return render(request, 'orders/payment.html')