from typing import Optional

from rest_framework import serializers

from apps.core.models import Item, ItemImage


class ItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image.image')

    def get_image(self, instance: Item) -> Optional[str]:
        item_image = ItemImage.objects.get_by_item_id(item_id=instance.id)
        if item_image and item_image.image.storage.exists(item_image.image.name):
            return item_image.image.url
        return None

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'category', 'image']
        read_only_fields = ['id', 'name', 'description', 'price', 'category', 'image']
