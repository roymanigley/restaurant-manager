from rest_framework import serializers

from apps.core.models import Item, ItemImage


class ItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(
        source='image.image', read_only=True, default=None)

    def get_image(self, instance: Item):
        item_image = ItemImage.objects.get_by_item_id(item_id=instance.id)
        if item_image:
            return item_image.image.url
        return None

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['image']
