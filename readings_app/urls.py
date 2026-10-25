from django.urls import path
from . import views

app_name = "readings"  # <--- ДОБАВИТЬ

urlpatterns = [
    path("", views.readings_list, name="list"),
]
