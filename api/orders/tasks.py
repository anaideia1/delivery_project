from config.celery import app

from api.orders.services import delayed_orders_change_status


@app.task(ignore_result=True)
def delayed_orders():
    """
    Celery task for updating statuses on delayed for all outdated orders with
    created status
    """
    res = delayed_orders_change_status()
    return f'Updated {res} orders' if res else 'Nothing has been updated'
