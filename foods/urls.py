from django.urls import path

from foods.views import FoodListView, FoodDetailView, FoodCreateView, FoodUpdateView

app_name = 'foods'

urlpatterns = [
    path('', FoodListView.as_view(), name='food_list'),
    path('category/<slug:category_slug>/', FoodListView.as_view(), name='foods_list_by_category'),
    path('new/', FoodCreateView.as_view(), name='food_create'),
    path('detail/<int:pk>/', FoodDetailView.as_view(), name='food_detail'),
    path('update/<int:pk>/', FoodUpdateView.as_view(), name='food_update'),
]