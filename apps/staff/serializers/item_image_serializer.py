from rest_framework import serializers

from apps.core.models import Item, ItemImage


class ItemImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='item.id', read_only=True)
    name = serializers.CharField(source='item.name', read_only=True)
    description = serializers.CharField(source='item.description', read_only=True)
    category = serializers.ChoiceField(source='item.category', choices=Item.Category.choices, read_only=True)
    price = serializers.FloatField(source='item.price', read_only=True)
    restaurant = serializers.IntegerField(source='item.restaurant.id', read_only=True)
    active = serializers.IntegerField(source='item.active', read_only=True)
    image = serializers.ImageField()

    # def to_representation(self, instance: ItemImage):
    #     representation = super().to_representation(instance)
    #     representation['id'] = instance.item.id
    #     representation['name'] = instance.item.name
    #     representation['description'] = instance.item.description
    #     representation['category'] = instance.item.category
    #     representation['price'] = instance.item.price
    #     representation['restaurant'] = instance.item.restaurant.id
    #     representation['active'] = instance.item.active
    #     return representation

    class Meta:
        model = ItemImage
        fields = [
            'id',
            'name',
            'description',
            'category',
            'price',
            'restaurant',
            'active',
            'image',
        ]
