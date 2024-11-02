from typing import Optional

from django.db import models

from apps.core.models import Item


class _CustomQuerySet(models.QuerySet):

    def get_by_item_id(self, *, item_id: int) -> Optional['ItemImage']:
        return self.filter(item_id=item_id).first()


class _CustomManager(models.Manager):

    def get_queryset(self) -> _CustomQuerySet['ItemImage']:
        return _CustomQuerySet(model=self.model)

    def get_by_item_id(self, *, item_id: int) -> Optional['ItemImage']:
        return self.get_queryset().get_by_item_id(item_id=item_id)


class ItemImage(models.Model):
    image = models.ImageField(upload_to='item-images')
    item = models.OneToOneField(Item, on_delete=models.CASCADE)

    objects = _CustomManager()

    def __str__(self):
        return f'{self.image.name} ({self.item.name})'
