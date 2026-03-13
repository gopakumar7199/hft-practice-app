import logging
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def process_trade(self, trade_id):
    """
    Async Celery task that processes a trade order.

    This runs on the Celery worker ECS service, consuming tasks
    from the shared ElastiCache Redis queue.

    In the real HFT system this would:
    - Validate the trade against risk limits
    - Connect to the broker API
    - Execute the order
    - Update the database
    - Send notifications via the Notification service
    """
    try:
        from apps.trades.models import Trade

        logger.info(f"Processing trade {trade_id}")
        trade = Trade.objects.get(id=trade_id)

        if trade.status != 'PENDING':
            logger.warning(f"Trade {trade_id} is not PENDING, skipping")
            return

        # Simulate trade execution
        trade.status     = 'EXECUTED'
        trade.executed_at = timezone.now()
        trade.notes      = f'Executed by Celery worker at {timezone.now()}'
        trade.save()

        logger.info(f"Trade {trade_id} executed successfully")
        return {'trade_id': trade_id, 'status': 'EXECUTED'}

    except Exception as exc:
        logger.error(f"Trade {trade_id} processing failed: {exc}")
        raise self.retry(exc=exc, countdown=5)
