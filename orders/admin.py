from django.contrib import admin
from .models import Order, OrderItem
from django.urls import path
from django.db import models
from django.shortcuts import render

from django.http import HttpResponse

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['food']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


class OrderVerify(models.Model):
    class Meta:
        verbose_name_plural = 'Orders to verify'

def unverified_orders_list(request):
    orders = Order.objects.filter(payment_by_cash=True, verified=False)
    return render(request, 'orders/verify_order.html', {'orders': orders})

class OrderVerifyAdmin(admin.ModelAdmin):
    model = OrderVerify

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name)
        
        return [
                path('orders-list/', unverified_orders_list, name=view_name),
            ]

admin.site.register(OrderVerify, OrderVerifyAdmin)