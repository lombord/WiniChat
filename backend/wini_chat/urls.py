from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from .static import range_serve
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('base_app.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          view=range_serve,
                          document_root=settings.MEDIA_ROOT)
