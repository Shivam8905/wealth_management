from django.core.exceptions import ValidationError
from django.db import models

"""
why 2 model Transaction and TransactionDetail ? 
-> Because most of the change are done on TransactionDetail, 
so data of Transaction is safe and can be use to see history.
"""

class TransactionType(models.IntegerChoices):
    """
    Enum for defining different types of transactions:
    - BUY: Increases the stock holding.
    - SELL: Decreases the stock holding.
    - SPLIT: Adjusts the quantity and price per share based on the split ratio.
    """
    BUY = 1, 'Buy'
    SELL = 2, 'Sell'
    SPLIT = 3, 'Split'

class Transaction(models.Model):
    """
    Represents a stock market transaction.

    Fields:
    - company: Name of the company (e.g., "ABC Ltd.")
    - date: Date of the transaction
    - trade_type: Type of trade (BUY, SELL, SPLIT)
    - quantity: Number of stocks involved in the transaction
    - price_per_share: Price per stock at the time of transaction
    - split_ratio: Used only for split transactions (format: "1:5")
    """
    company = models.CharField(max_length=120) # Name of the company
    date = models.DateField()
    trade_type = models.PositiveSmallIntegerField(choices=TransactionType.choices)
    quantity = models.IntegerField(null=True)
    price_per_share = models.DecimalField(max_digits=11, decimal_places=3, null=True) # Max value ~ 1 crore
    split_ratio = models.CharField(max_length=10, null=True)

    def clean(self):
        """
        Validates the transaction:
        - SELL type should have a positive quantity.
        - SPLIT type should have a valid split ratio.
        """
        if self.trade_type == TransactionType.SELL and self.quantity <= 0:
            raise ValidationError("Sell quantity must be greater than zero.")

        if self.trade_type == TransactionType.SPLIT and not self.split_ratio:
            raise ValidationError("Split ratio is required for SPLIT type.")

    def save(self, *args, **kwargs):
        """
          Clean and save the transaction.
          """
        self.clean()
        super().save(*args, **kwargs)


class TransactionDetail(models.Model):
    """
    Represents the state of stock holdings after each transaction.

    Fields:
    - active: Make it false if due to some issue you want to ignore any TransactionDetail
    - company: Name of the company
    - quantity: Number of stocks held
    - price_per_share: Average price per stock
    """
    active = models.BooleanField(default=True)
    company = models.CharField(max_length=120)
    quantity = models.IntegerField(null=True)
    price_per_share = models.DecimalField(max_digits=11, decimal_places=3) # Max value ~ 1 crore
