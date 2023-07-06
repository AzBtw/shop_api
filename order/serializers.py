from rest_framework import serializers
from .models import Order, OrderItem
from product.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = OrderItem
        fields = ('product', 'product_title', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    user_email = serializers.ReadOnlyField(source='owner.email')
    user = serializers.ReadOnlyField(source='owner.id')
    products = OrderItemSerializer(write_only=True, many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        products = validated_data.pop('products')
        user = self.context['request'].user
        total_sum = 0
        for product in products:
            total_sum += product['quantity'] * product['product'].price

        order = Order.objects.create(user=user, total_sum=total_sum, status = 'open', **validated_data)
        order_item_objects = [
            OrderItem(order=order, product=product['product'], quantity=product['quantity'])
            for product in products]
        OrderItem.objects.bulk_create(order_item_objects)
        return order

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['product'] = OrderItemSerializer(instance.items.all(), many=True)
        repr.pop('product')
        return repr
