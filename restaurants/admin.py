from django.contrib import admin
from .models import Category, Restaurant

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug', 'available', 'open_hour', 'close_hour',
                    'created', 'updated']
    list_filter = ['category', 'available', 'open_hour', 'close_hour', 'created', 'updated']
    list_editable = ['available', 'category']
    prepopulated_fields = {'slug': ('name',)}