from django.db import models


class Trade(models.Model):
    """
    Represents a single trade order in the HFT system.
    Mirrors what the real TradeEngine service manages.
    """
    TRADE_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('EXECUTED', 'Executed'),
        ('CANCELLED', 'Cancelled'),
        ('FAILED', 'Failed'),
    ]

    symbol      = models.CharField(max_length=20)
    trade_type  = models.CharField(max_length=4, choices=TRADE_TYPES)
    quantity    = models.DecimalField(max_digits=15, decimal_places=4)
    price       = models.DecimalField(max_digits=15, decimal_places=4)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at  = models.DateTimeField(auto_now_add=True)
    executed_at = models.DateTimeField(null=True, blank=True)
    notes       = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.trade_type} {self.quantity} {self.symbol} @ {self.price}"

    @property
    def total_value(self):
        return float(self.quantity) * float(self.price)
