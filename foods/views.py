from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from foods.models import Food, Category


class FoodListView(ListView):
    model = Food
    ordering = '-created'
    template_name = 'foods/food_list.html'
    context_object_name = 'foods'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self, **kwargs):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            return self.model.objects.filter(category=category)
        return self.model.objects.all()


class FoodDetailView(DetailView):
    model = Food
    template = 'foods/food_detail.html'
    context_object_name = 'food'


class FoodCreateView(CreateView):
    model = Food
    # ! Remove restaurant and obtain the current restaurant through authenticated user
    fields = ['category', 'name', 'description', 'price', 'image', 'available', 'restaurant']


class FoodUpdateView(UpdateView):
    model = Food
    # ! Remove restaurant and obtain the current restaurant through authenticated user
    fields = ['category', 'name', 'description', 'price', 'image', 'available', 'restaurant']    