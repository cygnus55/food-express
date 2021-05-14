from django.contrib import admin

from foods.models import Category, Food, FoodTemplate


@admin.register(Category)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'created', 'updated']
    list_editable = ['available', 'category']


@admin.register(FoodTemplate)
class FoodTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available']
    list_editable = ['available', 'category']