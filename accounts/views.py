from django.shortcuts import render, redirect, get_list_or_404
from .forms import UserForm, UserFormProfile, ProfileForm
from .models import User, Profile
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
#email verifications imports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from cart.views import _cart_id
from cart.models import Cart, CartItem
import requests
from orders.models import Order, OrderProduct

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = User.objects.createUser(first_name=first_name, last_name=last_name, 
                                       email=email, username=username, password=password)
            user.save()

            #Create Profile for user
            profile = Profile()
            profile.user_id = user.id
            profile.profile_image = '/default/default_profile.webp'
            profile.save()

            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/account_verification_email.html',
                                       {
                                           'user':user,
                                           'domain':current_site,
                                           'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token':default_token_generator.make_token(user)
                                       })
            to_email = email
            send_email = EmailMessage(mail_subject, message,to=[to_email])
            send_email.send()
            messages.success(request, "Thank you for registering, we have sent you a verification email to complete the registration process")
            return redirect('home')
        
    form = UserForm()
    context = {'form':form}
    

    return render(request, 'accounts/register.html', context)





# def activate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User._default_manager(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#        user = None
    
#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, "Congratulatons, Your account has been registerred successfully!")
#         return redirect('login')
#     else:
#         messages.error(request, "Invalid activation link")
#         return redirect('register')
    


def activate(request, uidb64, token):
    # Activate the user
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account has been activated")
        return redirect('login')
    else:
        messages.error(request, "Invalid Activation Link")
        return redirect('register')




def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user:
            try:
               
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()
                
                product_variations = []
                if is_cart_item_exist:
                    cart_item = CartItem.objects.filter(cart=cart)
                    #Getting product variation by cart_id
                    product_variations = []
                    for item in cart_item:
                        variations = item.variations.all()
                        product_variations.append(list(variations))
                        item.user = user
                        item.save()

                cart_item = CartItem.objects.filter( user=user)
            
                existing_var_list = []
                id = []
                for item in cart_item:
                    existing_variations = item.variations.all()
                
                    existing_var_list.append(list(existing_variations))
                    id.append(item.id)

                for pr in product_variations:
                    if pr in existing_var_list:
                        index = existing_var_list.index(pr)
                        cart_id = id[index]
                        item = CartItem.objects.get(id=cart_id)
                        item.quantity += 1
                        item.user = user
                        item.save()
                    else:
                        cart_item = CartItem.objects.filter(cart=cart)
                        for item in cart_item:
                            item.user = user
                            item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, "You are logged in now")
            url = request.META.get('HTTP_REFERER')
            try:
               query = requests.utils.urlparse(url).query
               params = dict(x.split('=') for x in query.split('&'))
               if 'next' in params:
                   nextPage = params['next']
                   return redirect(nextPage)


            except:
                return redirect('dashboard')  
       
        else:
            messages.error(request, "Valid credentials ")
    
    return render(request, 'accounts/login.html')



@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-date_created').filter(user_id = request.user.id, is_ordered=True)
    orders_count = orders.count()
    context = {'orders':orders, 'orders_count':orders_count}
    return render(request, 'accounts/dashboard.html', context)


def forgotPassword(request):
    if request.method == 'POST':
        email  = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact =email)
            current_site = get_current_site(request)
            mail_subject = "Please reset your password"
            message = render_to_string('accounts/reset_password_email.html',
                                       {
                                           'user':user,
                                           'domain':current_site,
                                           'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token':default_token_generator.make_token(user)
                                       })
            to_email = email
            send_email = EmailMessage(mail_subject, message,to=[to_email])
            send_email.send()
            messages.success(request, 'Password email has been sent to your email address !')
            return redirect('login')
        else:
            messages.error(request, 'Account with this email does not exist')
            return redirect('forgotPassword')

    return render(request, 'accounts/forgotPassword.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password!')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Invalid reset password link!')
        return redirect('login')
    


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetPassword')

    return render(request, 'accounts/resetPassword.html')

@login_required(login_url='login')
def logout(request):
  
    auth.logout(request)
    messages.info(request, 'You are logged out')
    
    return redirect('login')

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.order_by('-date_created').filter(user_id = request.user.id, is_ordered=True)
    orders_count = orders.count()
    context = {'orders':orders, 'orders_count':orders_count}

    return render(request, 'accounts/my_orders.html', context)


@login_required(login_url='login')
def edit_profile(request):
    # profile_instance=get_list_or_404(Profile, user=request.user)
    profile_instance = Profile.objects.get(user=request.user)
    if request.method == 'POST':

        user_form = UserFormProfile(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile_instance)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('edit_profile')
    else:
        user_form = UserFormProfile(instance=request.user)
        profile_form = ProfileForm(instance=profile_instance)
    context = {'user_form':user_form,
               'profile_form':profile_form,
               'profile_instance':profile_instance}
    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = User.objects.get(username__exact=request.user.username)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password Changed Successfully!')
                return redirect('dashboard')
            else:
                messages.error(request, "Current Password is Incorrect!")
                return redirect('change_password')
        else:
            messages.error(request, "Passwods do not match!")
            return redirect('change_password')
    
    return render(request, 'accounts/change_password.html')


@login_required(login_url="login")
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        "order_detail": order_detail,
        "order": order,
        "subtotal": subtotal,
    }
    return render(request, "accounts/order_detail.html", context)