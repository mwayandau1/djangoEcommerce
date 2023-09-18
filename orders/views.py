from django.shortcuts import render, redirect
from cart.models import CartItem, Cart
from .forms import OrdersForm
from store.models import Product
import datetime
from .models import Payment, Order, OrderProduct
import json
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import JsonResponse


def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    order_total = 0
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        order_total += (cart_item.product.price * cart_item.quantity)
        quantity = cart_item.quantity
        tax = order_total * (1 / 100)
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

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            data.order_number = current_date + str(data.id)
            data.save()
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=data.order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': order_total,
                'tax': tax,
                'grand_total': grand_total
            }
            return render(request, 'orders/payment.html', context)
        else:
            return redirect('checkout')


def payment(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    payment = Payment(user=request.user,
                      payment_id=body['transID'],
                      payment_method=body['payment_method'],
                      amount_paid=order.order_total,
                      status=body['status'])
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_item = CartItem.objects.filter(user=request.user)
    for item in cart_item:
        orderProduct = OrderProduct()
        orderProduct.order_id = order.id
        orderProduct.payment = payment
        orderProduct.user_id = request.user.id
        orderProduct.product_id = item.product_id
        orderProduct.quantity = item.quantity
        orderProduct.product_price = item.product.price
        orderProduct.ordered = True
        orderProduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variations = cart_item.variations.all()
        orderProduct = OrderProduct.objects.get(id=orderProduct.id)
        orderProduct.variations.set(product_variations)
        orderProduct.save()

        # Reduce the quantity of Product
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    # Clear Cart item
    cart_item = CartItem.objects.filter(user=request.user)
    cart_item.delete()
    # Send Order email message
    mail_subject = "Order Successful"
    message = render_to_string('orders/order_received_email.html',
                               {
                                   'user': request.user,
                                   'order': order

                               })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id
    }
    return JsonResponse(data)

    # return render(request, 'orders/payment.html')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        orderProduct = OrderProduct.objects.filter(order=order)
        payment = Payment.objects.get(payment_id=transID)
        subtotal = 0
        grand_total = 0
        for item in orderProduct:
            subtotal += item.product_price * item.quantity

        context = {
            'order': order,
            'orderProduct': orderProduct,
            'transID': payment.payment_id,
            'order_number': order.order_number,
            'user': request.user,
            'payment': payment,
            'subtotal': subtotal,

        }
        return render(request, 'orders/order_complete.html', context)

    except (Order.DoesNotExist, Payment.DoesNotExist):
        return redirect('store')
