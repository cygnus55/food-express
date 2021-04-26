from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    # urls for customers to view resturants
    path('', views.restaurant_list, name='restaurant_list'),
    path('<slug:category_slug>/', views.restaurant_list, name='restaurant_list_by_category'),
    path('<int:id>/<slug:slug>/', views.restaurant_detail, name='restaurant_detail'),
    # urls for restaurant user to view his/her restaurant
    path('dashboard/<str:username>/', views.restaurant_dashboard, name='restaurant_dashboard'),
    path('profile/<str:username>/', views.update_restaurant_profile, name='update_restaurant_profile' ),
]
