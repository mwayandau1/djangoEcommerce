
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # path('admin/', include('admin_honeypot'), namespace='admin_honeypot'),
    path('admin_secure/', admin.site.urls),
    path("", views.home, name="home"),
    path('accounts/',include('accounts.urls')),
    path('store/',include('store.urls')),
    path('cart/', include('cart.urls')),

    #Orders
    path('orders/', include('orders.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
