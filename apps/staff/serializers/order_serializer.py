from rest_framework import serializers

from apps.core.models import Order, ItemImage


class OrderSerializer(serializers.ModelSerializer):
    table_name = serializers.CharField(source='occupation__table__name', read_only=True)
    item_name = serializers.CharField(read_only=True, source='item.name')
    item_image = serializers.SerializerMethodField(default=None, read_only=True, source='item.image.image')

    def get_item_image(self, instance: Order):
        item_image = ItemImage.objects.get_by_item_id(item_id=instance.item.id)
        if item_image:
            return item_image.image.url
        return None

    class Meta:
        model = Order
        fields = '__all__'
