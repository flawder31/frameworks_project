from django.urls import path
from . import views

urlpatterns = [
    path("", views.meters_list, name="meters_list"),
    # Используем str, так как коды у нас текстовые (EL, CW)
    path("<str:meter_code>/", views.meter_detail, name="meter_detail"),
]
