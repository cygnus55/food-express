from django.urls import path

from delivery_person.views import home_view, mark_order_as_complete, mark_order_as_incomplete, delivery_person_profile_update

app_name = 'delivery_person'

urlpatterns = [
    path('home/', home_view, name='home'),
    path('profile/', delivery_person_profile_update, name='profile_update'),
    path(
        'mark-order-as-complete/<int:order_id>', 
        mark_order_as_complete, 
        name='mark_order_as_complete'
    ),
    path(
        'mark-order-as-incomplete/<int:order_id>', 
        mark_order_as_incomplete, 
        name='mark_order_as_incomplete'
    ),
]