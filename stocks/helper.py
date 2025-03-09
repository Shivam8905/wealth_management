from decimal import Decimal

from .models import  TransactionDetail, TransactionType


def buy_handler(transaction):
    """
    Handles BUY transactions.
    - Adds a new stock holding.
    """
    TransactionDetail.objects.create(
        company=transaction.company,
        quantity=transaction.quantity,
        price_per_share=transaction.price_per_share
    )


def sell_handler(transaction):
    """
    Handles SELL transactions.
    - Uses FIFO (First In, First Out) to reduce holdings.
    - Deletes fully sold stocks to keep the table clean.
    """
    holdings = TransactionDetail.objects.filter(
        company=transaction.company,
        active=True
    ).order_by('id')  # FIFO order

    qty_to_sell = transaction.quantity

    # Ensure there are enough stocks to sell
    total_holdings = sum(holding.quantity for holding in holdings)

    if qty_to_sell > total_holdings:
        raise ValueError(f"Cannot sell {qty_to_sell} stocks. Only {total_holdings} available.")

    while qty_to_sell > 0 and holdings.exists():
        holding = holdings.first()

        if holding.quantity <= qty_to_sell:
            # If the full quantity is sold, remove the record
            qty_to_sell -= holding.quantity
            holding.delete()
        else:
            # If partially sold, reduce the quantity and keep the record
            holding.quantity -= qty_to_sell
            holding.save()
            qty_to_sell = 0


def split_handler(transaction):
    """
    Handles SPLIT transactions.
    - Adjusts the quantity and price based on the split ratio.
    """
    holdings = TransactionDetail.objects.filter(company=transaction.company, active=True)

    try:
        split_ratio = transaction.split_ratio.split(':')
        if len(split_ratio) != 2:
            raise ValueError("Invalid split ratio format. Use format like '1:5'")
        multiplier = int(split_ratio[1]) / int(split_ratio[0])
    except (ValueError, IndexError):
        raise ValueError("Invalid split ratio format. Use format like '1:5'")


    for holding in holdings:
        holding.quantity = int(holding.quantity * multiplier)
        holding.price_per_share = holding.price_per_share / Decimal(multiplier)
        holding.save()


def get_average_price_and_balance(company):
    """
    Returns the average price and balance quantity for a company.
    """
    holdings = TransactionDetail.objects.filter(company=company, active=True)
    total_quantity = sum(holding.quantity for holding in holdings)
    if total_quantity == 0:
        return 0, 0
    total_cost = sum(holding.quantity * holding.price_per_share for holding in holdings)
    avg_price = total_cost / total_quantity
    return avg_price, total_quantity


"""
In future if you want to add any new functionality.
1. Add in TransactionType Enum
2. Make a new function
3. Add in TRANSACTION_HANDLER
"""
TRANSACTION_HANDLER = {
    TransactionType.BUY: buy_handler,
    TransactionType.SELL: sell_handler,
    TransactionType.SPLIT: split_handler
}

