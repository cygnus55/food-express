from django.urls import path

from . import views
from location.views import add_delivery_location, update_delivery_location
from customer.views import fav_restaurant, fav_food, unfav_food, unfav_restaurant

app_name = 'customer'

urlpatterns = [
    path('home/', views.customer_homepage, name='homepage'),
    path(
        'profile/',
        views.customer_profile_update,
        name='profile_update'
    ),
    path(
        'orderhistory/',
        views.orderhistory,
        name='order_history'
    ),
    path(
        'add-delivery-location/',
        add_delivery_location,
        name='add_delivery_location'
    ),
    path(
        'delivery-location/<int:location_id>/',
        update_delivery_location,
        name='update_delivery_location'
    ),
    path(
        'fav/restaurant/<int:pk>',
        fav_restaurant,
        name='fav_restaurant'
    ),
    path(
        'fav/food/<int:pk>',
        fav_food,
        name='fav_food'
    ),
    path(
        'unfav/restaurant/<int:pk>',
        unfav_restaurant,
        name='unfav_restaurant'
    ),
    path(
        'unfav/food/<int:pk>',
        unfav_food,
        name='unfav_food'
    )
]
