from django.urls import path
from . import views
from location.views import add_delivery_location, update_delivery_location

app_name = 'customer'

urlpatterns = [
    path('home/', views.customer_homepage, name='homepage'),
    path(
        'profile/',
        views.customer_profile_update,
        name='profile_update'
    ),
    path('add-delivery-location/',
        add_delivery_location,
        name="add_delivery_location"),
    path('delivery-location/<int:location_id>/',
        update_delivery_location,
        name="update_delivery_location"),
]
