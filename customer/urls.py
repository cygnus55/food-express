from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('home/', views.customer_homepage, name='homepage'),
]
