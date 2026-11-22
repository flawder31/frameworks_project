from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Добавь это
from django.conf.urls.static import static # И это

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')), # Главная страница
    path('meters/', include('meters_app.urls')),
    path('readings/', include('readings_app.urls')),
]

# ВАЖНО: Эта строка нужна, чтобы Django отдавал CSS/JS файлы при DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Подключение Debug Toolbar (если ты его ставил)
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass