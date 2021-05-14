# from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .decorators import restaurant_required
from .models import Category, Restaurant
from accounts.models import User
from .forms import RestaurantProfileForm
from foods.models import Food, FoodTemplate, Category as FoodCategory
from foods.views import FoodListView, FoodDetailView

def restaurant_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    # currentTime = datetime.now().time()
    restaurants = Restaurant.objects.all()
    # tmp_restaurant1 = tmp_restaurant.filter(Q(open_hour__lte=F('close_hour')), Q(open_hour__lte=currentTime), close_hour__gte=currentTime)
    # tmp_restaurant2 = tmp_restaurant.filter(available=True).filter(Q(open_hour__gt=F('close_hour')), Q(open_hour__lte=currentTime) | Q(close_hour__gte=currentTime))
    # restaurants = tmp_restaurant1 | tmp_restaurant2
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        restaurants = restaurants.filter(category=category)
    return render(
        request,
        'restaurants/restaurant_list.html',
        {
            'category': category,
            'categories': categories,
            'restaurants': restaurants
        }
    )

def restaurant_detail(request, id, slug):
    restaurant = get_object_or_404(Restaurant,
                                id=id,
                                slug=slug)

    foods_obj = Food.objects.filter(restaurant=restaurant)
    food_categories = set(map(lambda x: x.category, foods_obj))

    foods = {}

    for category in food_categories:
        foods[category.name] = []
    
    for food in foods_obj:
        foods[food.category.name].append(food)

    return render(request,
                'restaurants/restaurant_detail.html',
                {'restaurant': restaurant,
                'foods': foods,
                })

@login_required
@restaurant_required
def restaurant_dashboard(request, username):
    restaurant = User.objects.get(username=username)
    context={
        'restaurant': restaurant,
        'section': 'dashboard',
    }
    return render (request, 'restaurants/dashboard.html',context)

@login_required
@restaurant_required
def update_restaurant_profile(request, username):
    restaurant = Restaurant.objects.get(user__username=username)
    if request.method == 'GET':
        form = RestaurantProfileForm(instance=restaurant)
    else:
        form = RestaurantProfileForm(data=request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile Update Successful')
            return redirect('restaurants:restaurant_dashboard', username=username)

    context={
        'form': form,
        'section': 'profile',
    }
    return render (request, 'restaurants/profile_update.html',context)


class FoodCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Food
    fields = ['category', 'name', 'description', 'price', 'image', 'available']
    template_name = 'restaurants/food_form.html'
    success_url = reverse_lazy('restaurants:food_list')

    def test_func(self):
        return self.request.user.is_active and self.request.user.is_restaurant
    
    def form_valid(self, form):
        form.instance.restaurant = self.request.user.restaurant
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        template_slug = self.kwargs.get('slug')
        context =  super().get_context_data(**kwargs)
        context['templates'] = FoodTemplate.objects.all()
        context['template_slug'] = template_slug 
        return context


class FoodUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Food
    fields = ['category', 'name', 'description', 'price', 'image', 'available']
    template_name = 'restaurants/food_form.html'
    success_url = reverse_lazy('restaurants:food_list')

    def test_func(self):
        return self.request.user.is_active and self.request.user.is_restaurant \
            and self.get_object().restaurant == self.request.user.restaurant
    
    def form_valid(self, form):
        form.instance.restaurant = self.request.user.restaurant
        return super().form_valid(form)


class FoodDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Food
    success_url = reverse_lazy('restaurants:food_list')
    context_object_name = 'form'
    template_name = 'restaurants/food_delete.html'

    def test_func(self):
        return self.request.user.is_active and self.request.user.is_restaurant \
            and self.get_object().restaurant == self.request.user.restaurant


class RestaurantFoodListView(LoginRequiredMixin, UserPassesTestMixin, FoodListView):
    template_name = 'restaurants/food_list.html'

    def test_func(self):
        return self.request.user.is_active and self.request.user.is_restaurant

    def get_queryset(self, **kwargs):
        restaurant_foods = self.model.objects.filter(restaurant=self.request.user.restaurant)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(FoodCategory, slug=category_slug)
            return restaurant_foods.filter(category=category)
        return restaurant_foods.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('category_slug')
        restaurant_foods = self.model.objects.filter(restaurant=self.request.user.restaurant)
        categories = set(map(lambda x: x.category, restaurant_foods))
        context['categories'] = categories
        if slug:
            context['category'] = get_object_or_404(FoodCategory, slug=slug)
        return context


class RestaurantFoodDetailView(LoginRequiredMixin, UserPassesTestMixin, FoodDetailView):
    template_name = 'restaurants/food_detail.html'

    def test_func(self):
        return self.request.user.is_active and self.request.user.is_restaurant \
            and self.get_object().restaurant == self.request.user.restaurant