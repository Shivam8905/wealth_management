from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from .models import Transaction
from .serializers import TransactionSerializer
from .helper import get_average_price_and_balance, TRANSACTION_HANDLER


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()

        # Handles transaction based on type using TRANSACTION_HANDLER
        transaction_handler = TRANSACTION_HANDLER.get(transaction.trade_type)
        if transaction_handler:
            try:
                transaction_handler(transaction)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='average-price')
    def average_price(self, request):
        company = request.query_params.get('company')
        if not company:
            return Response({'error': 'Company parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        avg_price, balance_qty = get_average_price_and_balance(company)
        return Response({
            'company': company,
            'average_price': avg_price,
            'balance_quantity': balance_qty
        })
