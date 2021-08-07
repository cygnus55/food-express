from django.contrib import admin

from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_customer', 'is_restaurant', 'is_delivery_person']
    search_fields = ['email', 'username']
    list_filter = ['is_customer', 'is_restaurant', 'is_delivery_person']