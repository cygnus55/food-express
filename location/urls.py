from django.urls import path
from . import views

app_name = 'location'

urlpatterns = [
    path("ajax/get_place/", views.get_coords_place, name="get_coords_place"),
]
