from django.contrib import admin
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from django.db import models
from django.shortcuts import render

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['food']

def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f"<a href='{url}'>PDF</a>")
order_pdf.short_description = 'Invoice'

def order_detail(obj):
    url = reverse('orders:order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View detail</a>')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'created', 'updated', 'complete', 'payment_by_cash', 'verified', order_detail, order_pdf]
    list_filter = ['created', 'updated', 'verified', 'payment_by_cash', 'complete']
    inlines = [OrderItemInline]


# order to verify link added to admin page


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