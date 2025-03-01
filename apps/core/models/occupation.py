import uuid

from django.db import models
from django.db.models import Q
from django.utils.timezone import now

from apps.core.models.restaurant_user import RestaurantUser
from apps.core.models.table import Table


class _CustomQuerySet(models.QuerySet):

    def get_by_restaurant_id(self, *, restaurant_id: int) -> '_CustomQuerySet[Occupation]':
        return self.filter(table__restaurant_id=restaurant_id)

    def get_by_table_id(self, *, table_id: int) -> '_CustomQuerySet[Occupation]':
        return self.filter(table_id=table_id)

    def is_occupation_active(self, *, occupation_id: int) -> '_CustomQuerySet[Occupation]':
        is_active_filter = (Q(start__lte=now()) & Q(
            Q(end__isnull=True)
            |
            Q(end__gte=now())
        )
                            )
        return self.filter(id=occupation_id).filter(is_active_filter).exists()


class _CustomManager(models.Manager):

    def get_queryset(self) -> _CustomQuerySet['Occupation']:
        return _CustomQuerySet(model=self.model)

    def get_by_restaurant_id(self, *, restaurant_id: int) -> _CustomQuerySet['Occupation']:
        return self.get_queryset().get_by_restaurant_id(restaurant_id=restaurant_id)

    def get_by_table_id(self, *, table_id: int) -> _CustomQuerySet['Occupation']:
        return self.get_queryset().get_by_table_id(table_id=table_id)

    def is_occupation_active(self, *, occupation_id: int) -> '_CustomQuerySet[Occupation]':
        return self.get_queryset().is_occupation_active(occupation_id=occupation_id)


class Occupation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    waiter = models.ForeignKey(RestaurantUser, on_delete=models.DO_NOTHING)

    objects = _CustomManager()

    def __str__(self):
        return f'{self.start} - {self.end} {self.table}'

    class Meta:
        ordering = ('-start',)
