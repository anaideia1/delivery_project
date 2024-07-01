from rest_framework import serializers

from api.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model
    """
    delivery_date = serializers.DateField()

    class Meta:
        model = Order
        fields = ('id', 'sku', 'name', 'price', 'delivery_date', 'status')
        readonly_field = ('id', 'status')

    def create(self, validated_data):
        return Order.objects.create(**validated_data)
