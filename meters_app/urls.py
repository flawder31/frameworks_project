from django.urls import path
from . import views

app_name = "meters"  # <--- ДОБАВИТЬ

urlpatterns = [
    path("", views.meters_list, name="list"),
    path("<str:meter_code>/", views.meter_detail, name="detail"),
]
