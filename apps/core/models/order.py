from django.db import models

from apps.core.models.item import Item
from apps.core.models.occupation import Occupation


class _CustomQuerySet(models.QuerySet):

    def get_by_restaurant_id(self, *, restaurant_id: int) -> models.QuerySet['Order']:
        return self.filter(occupation__table__restaurant_id=restaurant_id)

    def get_by_table_id(self, *, table_id: int) -> models.QuerySet['Order']:
        return self.filter(occupation__table_id=table_id)

    def get_by_occupation_id(self, *, occupation_id: int) -> models.QuerySet['Order']:
        return self.filter(occupation_id=occupation_id)


class _CustomManager(models.Manager):

    def get_queryset(self) -> models.QuerySet['Order']:
        return _CustomQuerySet(model=self.model)

    def get_by_restaurant_id(self, *, restaurant_id: int) -> models.QuerySet['Order']:
        return self.get_queryset().get_by_restaurant_id(restaurant_id=restaurant_id)

    def get_by_table_id(self, *, table_id: int) -> models.QuerySet['Order']:
        return self.get_queryset().get_by_table_id(table_id=table_id)

    def get_by_occupation_id(self, *, occupation_id: int) -> models.QuerySet['Order']:
        return self.get_queryset().get_by_occupation_id(occupation_id=occupation_id)


class Order(models.Model):
    class State(models.TextChoices):
        OPEN = 'OPEN'
        IN_PROGRESS = 'IN_PROGRESS'
        COMPETED = 'COMPLETED'
        CANCELED = 'CANCELED'

    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE)
    state = models.CharField(max_length=255, choices=State.choices, default=State.OPEN)
    amount = models.PositiveIntegerField()
    price_per_item = models.FloatField()

    objects = _CustomManager()

    def __str__(self):
        return f'{self.item.name} ({self.occupation})'

    class Meta:
        ordering = ('-occupation__start',)
