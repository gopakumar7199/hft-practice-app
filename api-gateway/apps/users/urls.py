from django.urls import path
from .views import ServiceInfoView

urlpatterns = [
    path('info/', ServiceInfoView.as_view(), name='service-info'),
]
