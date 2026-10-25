from django.urls import path
from . import views

app_name = "readings"

urlpatterns = [
    path("", views.readings_list, name="list"),
    path("add/", views.add_reading, name="add"),
    path("<int:reading_id>/delete/", views.delete_reading,
         name="delete"),  # <--- НОВЫЙ МАРШРУТ
]
