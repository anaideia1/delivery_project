import datetime
from django.db import models


class OrderQuerySet(models.QuerySet):
    """
    QuerySet for Order model manager.
    """
    def created(self):
        return self.filter(status=self.model.CREATED)

    def delayed(self):
        return self.filter(status=self.model.DELAYED)


class OrderManager(models.Manager):
    """
    Order model manager.
    """
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def filter_outdated_created_orders(self):
        return self.get_queryset().created().filter(
            delivery_date__lt=datetime.datetime.now()
        )
