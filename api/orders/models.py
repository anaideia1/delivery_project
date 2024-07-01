from django.db import models
from django.core.validators import MinLengthValidator

from api.orders.managers import OrderManager


class Order(models.Model):
    """
    Model for representing Order for delivery product
    """
    CREATED = 'created'
    DELAYED = 'delayed'
    STATUS_CHOICES = (
        (CREATED, 'Created'),
        (DELAYED, 'Delayed'),
    )

    sku = models.CharField(
        max_length=8,
        unique=True,
        validators=(MinLengthValidator(8), )
    )
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    delivery_date = models.DateField(db_index=True)
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default=CREATED
    )

    objects = OrderManager()

    def __str__(self):
        return f'Order {self.id}: {self.name} to {self.delivery_date}'
