from django.urls import path

from delivery_person.views import home_view, mark_order_as_complete, mark_order_as_incomplete, delivery_person_profile_update, delivery_person_order_detail, designate_order_to_delivery_person

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
    path(
        'order_detail/<int:order_id>/',
        delivery_person_order_detail,
        name='order_detail',
    ),
    path(
        'designate/<int:order_id>/',
        designate_order_to_delivery_person,
        name='designate_delivery_person',
    )
]