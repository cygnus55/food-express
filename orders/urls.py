from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path("create/", views.order_create_cash_payment, name="order_create"),
    path("create/pay-by-khalti/<str:token>/", views.order_create_khalti_payment, name="order_create_khalti_payment"),
    path("ajax/verify-payment/", views.verify_payment, name='verify_payment'),
    path("order_detail/<int:order_id>/", views.order_detail, name='order_detail'),
    path("order_detail/<int:order_id>/verify/", views.verify_order, name="verify_order"),
]
