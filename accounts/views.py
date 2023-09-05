from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
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

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = User.objects.create(first_name=first_name, last_name=last_name, 
                                       email=email, username=username, password=password)
            user.save()

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
            messages.success(request, "Your account has been created successfully!!!")
            return redirect('home')
        
    form = UserForm()
    context = {'form':form}
    

    return render(request, 'accounts/register.html', context)





def activate(request):
    return 



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
           # messages.success(request, 'You are logged in')
            return redirect('home')
        else:
            messages.error(request, "Valid credentials ")
    
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
  
    auth.logout(request)
    messages.info(request, 'You are logged out')
    
    return redirect('login')

