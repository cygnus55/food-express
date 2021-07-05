from os import name
from django.urls import path
from . import views


app_name = 'coupons'


urlpatterns = [
    path('apply/', views.coupon_apply, name='apply'),
    path('unapply/', views.coupon_unapply, name='unapply'),
    path('ajax-verify-coupon/', views.verify_coupon, name='ajax_verify_coupon'),
]