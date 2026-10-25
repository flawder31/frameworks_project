from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("meters/", include("meters_app.urls")),
    path("readings/", include("readings_app.urls")),
]

# Обработчик 404
handler404 = "homepage.views.page_not_found"