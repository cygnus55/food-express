from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('home/', views.customer_homepage, name='homepage'),
    path(
        'profile/<str:username>',
        views.customer_profile_update,
        name='profile_update'
    ),
]
