from rest_framework import serializers
from .models import Trade


class TradeSerializer(serializers.ModelSerializer):
    total_value = serializers.ReadOnlyField()

    class Meta:
        model  = Trade
        fields = [
            'id', 'symbol', 'trade_type', 'quantity',
            'price', 'total_value', 'status',
            'created_at', 'executed_at', 'notes'
        ]
        read_only_fields = ['id', 'created_at', 'executed_at', 'total_value']
