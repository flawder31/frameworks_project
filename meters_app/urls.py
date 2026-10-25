from django.urls import path
from . import views

app_name = "meters"
urlpatterns = [
    path("", views.meters_list, name="list"),
    path("add/", views.add_meter, name="add"),
    path("<str:meter_code>/", views.meter_detail, name="detail"),
    path("<str:meter_code>/delete/", views.delete_meter, name="delete"),
]
