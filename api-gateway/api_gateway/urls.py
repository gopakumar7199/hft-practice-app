from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.health.urls')),
    path('api/trades/', include('apps.trades.urls')),
    path('api/users/', include('apps.users.urls')),
]
