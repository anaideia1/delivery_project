from django.core.management.base import BaseCommand

from api.orders.tasks import delayed_orders


class Command(BaseCommand):
    def handle(self, *args, **options):
        delayed_orders.apply_async()
        print('Celery task was created.')
