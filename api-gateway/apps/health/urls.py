from django.urls import path
from .views import HealthCheckView, ReadinessView

urlpatterns = [
    path('', HealthCheckView.as_view(), name='health'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('ready/', ReadinessView.as_view(), name='readiness'),
]
