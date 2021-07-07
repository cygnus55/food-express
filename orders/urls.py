from os import name
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path("create/", views.order_create_cash_payment, name="order_create"),
    path("create/pay-by-khalti/<str:token>/", views.order_create_khalti_payment, name="order_create_khalti_payment"),
    path("ajax/verify-payment/", views.verify_payment, name='verify_payment'),
    path("order_detail/<int:order_id>/", views.order_detail, name='order_detail'),
    path("order_detail/<int:order_id>/verify/", views.verify_order, name="verify_order"),
    path("create/buynow/<int:food_id>/<int:quantity>/", views.order_create_buy_now, name="order_create_buy_now"),
    path("create/buynow/<int:food_id>/<int:quantity>/<str:coupon>/", views.order_create_buy_now, name="order_create_buy_now_coupon"),
    path("create/buynow/pay-by-khalti/<int:food_id>/<int:quantity>/<str:token>/", views.order_create_buy_now_khalti_payment,name="order_create_buy_now_khalti_payment"),
    path("create/buynow/pay-by-khalti/<int:food_id>/<int:quantity>/<str:token>/<str:coupon>", views.order_create_buy_now_khalti_payment,name="order_create_buy_now_khalti_payment_coupon"),

    path('admin/order/<int:order_id>/invoice/', views.admin_order_pdf, name='admin_order_pdf')
]
