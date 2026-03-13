import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Trade
from .serializers import TradeSerializer
from .tasks import process_trade

logger = logging.getLogger(__name__)


class TradeViewSet(viewsets.ModelViewSet):
    """
    Trade management API.
    POST /api/trades/         — create a new trade order
    GET  /api/trades/         — list all trades
    GET  /api/trades/{id}/    — get a specific trade
    POST /api/trades/{id}/execute/ — execute a pending trade (async via Celery)
    """
    queryset         = Trade.objects.all()
    serializer_class = TradeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trade = serializer.save()

        logger.info(f"Trade created: {trade.id} — {trade.trade_type} {trade.quantity} {trade.symbol}")

        # Send to Celery for async processing via ElastiCache Redis
        try:
            process_trade.delay(trade.id)
            logger.info(f"Trade {trade.id} queued for processing")
        except Exception as e:
            logger.warning(f"Could not queue trade {trade.id}: {e} — Redis may not be available locally")

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        trade = self.get_object()
        if trade.status != 'PENDING':
            return Response(
                {'error': f'Trade is {trade.status}, only PENDING trades can be executed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            process_trade.delay(trade.id)
            return Response({'message': f'Trade {trade.id} queued for execution'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Returns a summary of trades by status — used by the dashboard."""
        from django.db.models import Count, Sum
        summary = Trade.objects.values('status').annotate(
            count=Count('id'),
            total_value=Sum('price')
        )
        return Response(list(summary))
