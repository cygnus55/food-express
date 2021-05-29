from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path("create/<str:payment>/", views.order_create, name="order_create"),
    path("ajax/order-list/", views.order_list, name='ajax_order_list'),
    path("order_detail/<int:order_id>/", views.order_detail, name='order_detail'),
    path("order_detail/<int:order_id>/verify/", views.verify_order, name="verify_order"),
]
