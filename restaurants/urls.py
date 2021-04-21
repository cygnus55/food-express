from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path("", views.restaurant_list, name="restaurant_list"),
    path('<slug:category_slug>/', views.restaurant_list, name="restaurant_list_by_category"),
    path("<int:id>/<slug:slug>/", views.restaurant_detail, name="restaurant_detail"),
    path('dashboard/<str:username>', views.restaurant_dashboard, name='restaurant_dashboard'),
]
