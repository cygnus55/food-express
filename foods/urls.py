from django.urls import path

from foods.views import FoodListView, FoodDetailView

app_name = 'foods'

urlpatterns = [
    path('', FoodListView.as_view(), name='food_list'),
    path('category/<slug:category_slug>/', FoodListView.as_view(), name='foods_list_by_category'),
    path('detail/<int:pk>/', FoodDetailView.as_view(), name='food_detail'),
]