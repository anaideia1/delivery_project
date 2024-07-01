from api.orders.models import Order


def delayed_orders_change_status():
    """
    Update all outdated orders with status created to delayed status
    return: number of updated elements
    """
    return Order.objects.filter_outdated_created_orders().update(
        status=Order.DELAYED
    )

