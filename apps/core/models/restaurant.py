from typing import Optional

from django.db import models


class _CustomQuerySet(models.QuerySet):

    def get_active(self) -> '_CustomQuerySet[Restaurant]':
        return self.filter(active=True)

    def get_by_restaurant_id(self, *, restaurant_id: int) -> '_CustomQuerySet[Restaurant]':
        return self.filter(id=restaurant_id)

    def get_by_occupation_id(self, *, occupation_id: int) -> '_CustomQuerySet[Restaurant]':
        return self.filter(table__occupation__id=occupation_id).first()


class _CustomManager(models.Manager):

    def get_queryset(self) -> _CustomQuerySet['Restaurant']:
        return _CustomQuerySet(model=self.model)

    def get_active(self) -> _CustomQuerySet['Restaurant']:
        return self.get_queryset().get_active()

    def get_by_restaurant_id(self, *, restaurant_id: int) -> _CustomQuerySet['Restaurant']:
        return self.get_queryset().get_by_restaurant_id(restaurant_id=restaurant_id)

    def get_by_occupation_id(self, *, occupation_id: int) -> Optional['Restaurant']:
        return self.get_queryset().get_by_occupation_id(occupation_id=occupation_id)


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    objects = _CustomManager()

    def __str__(self):
        return f'{self.name}'
