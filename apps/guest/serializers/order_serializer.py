from rest_framework import serializers
from rest_framework.fields import CharField, SerializerMethodField

from apps.core.models import ItemImage, Order


class OrderSerializer(serializers.ModelSerializer):
    item_name = CharField(read_only=True, source='item.name')
    item_image = SerializerMethodField(default=None, read_only=True, source='item.image.image')

    def get_item_image(self, instance: Order):
        item_image = ItemImage.objects.get_by_item_id(item_id=instance.item.id)
        if item_image:
            return item_image.image.url
        return None

    def create(self, validated_data):
        validated_data['price_per_item'] = validated_data['item'].price
        validated_data['state'] = Order.State.OPEN
        validated_data['occupation_id'] = self.context['occupation_id']
        return super().create(validated_data)

    class Meta:
        model = Order
        fields = ['id', 'state', 'item_name', 'price_per_item', 'item_image', 'amount', 'item']
        create_only_fields = ['item']
        read_only_fields = ['state', 'item_name', 'price_per_item', 'item_image', 'id']
