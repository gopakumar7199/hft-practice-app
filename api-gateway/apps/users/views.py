import os
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response


class ServiceInfoView(APIView):
    """
    Returns information about this service instance.
    Useful for verifying which ECS task is serving the request.
    """
    def get(self, request):
        return Response({
            'service':      'hft-api-gateway',
            'version':      '1.0.0',
            'environment':  os.environ.get('ENVIRONMENT_TYPE', 'local'),
            'celery_broker': os.environ.get('CELERY_BROKER_URL', 'not-configured'),
            'database':     'connected' if self._check_db() else 'not-connected',
            'endpoints': {
                'health':   '/',
                'trades':   '/api/trades/',
                'info':     '/api/users/info/',
            }
        })

    def _check_db(self):
        try:
            from django.db import connection
            connection.ensure_connection()
            return True
        except Exception:
            return False
