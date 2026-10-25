from django.urls import path
from . import views

urlpatterns = [
    path("", views.readings_list, name="readings_list"),
]
