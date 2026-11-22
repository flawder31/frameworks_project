from django.urls import path
from . import views

app_name = "meters"

urlpatterns = [
    path("", views.meters_list, name="list"),
    path("add/", views.add_meter, name="add"),
    # Изменили <meter_code> на <slug:slug>
    path("<slug:slug>/", views.meter_detail, name="detail"),
    path("<slug:slug>/delete/", views.delete_meter, name="delete"),
]