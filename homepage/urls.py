from django.urls import path
from . import views

app_name = "homepage"  # <--- ДОБАВИТЬ

urlpatterns = [
    path("", views.index, name="index"),
]
