from django.urls import path
from base import views 

app_name = 'base'


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
]
