import os
import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class HealthCheckView(View):
    """
    Health check endpoint used by:
    - ALB target group health checks
    - ECS container health checks
    - CloudWatch synthetic monitors
    Returns 200 so ALB marks the task as healthy.
    """
    def get(self, request):
        return JsonResponse({
            'status': 'healthy',
            'service': 'hft-api-gateway',
            'environment': os.environ.get('ENVIRONMENT_TYPE', 'local'),
            'version': '1.0.0',
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class ReadinessView(View):
    """
    Readiness check — verifies database connectivity.
    ECS uses this to decide if traffic should be sent to this task.
    """
    def get(self, request):
        try:
            from django.db import connection
            connection.ensure_connection()
            db_status = 'connected'
        except Exception as e:
            db_status = f'error: {str(e)}'

        is_ready = db_status == 'connected'
        return JsonResponse({
            'status': 'ready' if is_ready else 'not_ready',
            'database': db_status,
            'service': 'hft-api-gateway',
        }, status=200 if is_ready else 503)
