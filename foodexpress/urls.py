"""foodexpress URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # new
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('', include('base.urls', namespace='base')),
    path('', include('accounts.urls', namespace='accounts')),
    path('restaurants/', include('restaurants.urls', namespace='restaurants')),
    path('customer/', include('customer.urls', namespace='customer')),
    path('foods/', include('foods.urls', namespace='foods')),
    path('location/', include('location.urls', namespace='location')),
]

#debug mode only not suitable for production
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'base.views.handler404'