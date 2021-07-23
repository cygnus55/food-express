from django.contrib import admin
from django.db import models
from django.urls import path

from delivery_person.models import DeliveryPerson, OrdersDesignation
from delivery_person.views import register


class RegisterDeliveryUser(models.Model):
    class Meta:
        verbose_name_plural = 'Register Delivery Users'


class RegisterDeliveryUserAdmin(admin.ModelAdmin):
    model = RegisterDeliveryUser

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name)
        return [
                path('register/', register, name=view_name),
            ]


@admin.register(OrdersDesignation)
class OrdersDesignationAdmin(admin.ModelAdmin):
    list_display = ['delivery_person', 'order']

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(DeliveryPerson)
admin.site.register(RegisterDeliveryUser, RegisterDeliveryUserAdmin)