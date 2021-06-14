from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required

from foods.models import Food, Category
from cart.forms import CartAddFoodForm, BuyNowForm
from customer.decorators import customer_required


class FoodListView(ListView):
    model = Food
    ordering = '-created'
    template_name = 'foods/food_list.html'
    context_object_name = 'foods'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('category_slug')
        context['categories'] = Category.objects.all()
        if slug:
            context['category'] = get_object_or_404(Category, slug=slug)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_food_form'] = CartAddFoodForm() 
        return context


@login_required
@customer_required
def buy_now(request):
    food_id = request.GET.get('id')
    quantity = request.GET.get('quantity')
    if not food_id or not quantity:
        return redirect('cart:cart_detail')
    food = get_object_or_404(Food, id=food_id)
    form = BuyNowForm(init)