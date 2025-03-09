from rest_framework import serializers
from .models import Transaction, TransactionDetail, TransactionType


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def validate(self, data):
        """
        Custom validation:
        - Ensure sell quantity does not exceed available stocks.
        - Validate split ratio format.
        """
        if data['trade_type'] == TransactionType.SELL:
            total_holdings = sum(
                h.quantity for h in TransactionDetail.objects.filter(company=data['company'], active=True)
            )
            if data['quantity'] > total_holdings:
                raise serializers.ValidationError(
                    {"Check Stock": "Sell quantity exceeds available holdings Or you don't have stock of this company"}
                )


        # Split ratio format validation
        if data['trade_type'] == TransactionType.SPLIT:
            split_ratio = data.get('split_ratio')
            if not split_ratio or ':' not in split_ratio:
                raise serializers.ValidationError(
                    {"Check Payload": "Invalid split ratio format. Use format like '1:5'"}
                )

        return data

class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetail
        fields = '__all__'







