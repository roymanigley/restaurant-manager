import datetime

from django.db import models
from django.db.models import Q

from apps.core.models.restaurant import Restaurant


class _CustomQuerySet(models.QuerySet):

    def get_by_restaurant_id(self, *, restaurant_id: int) -> models.QuerySet['Table']:
        return self.filter(restaurant_id=restaurant_id)

    def get_active(self) -> models.QuerySet['Table']:
        return self.filter(active=True)

    def get_available_tables(
            self, *, date_time: datetime.datetime
    ) -> models.QuerySet['Table']:
        return self.filter(active=True).exclude(
            Q(occupation__start__lte=date_time)
            & (
                    Q(occupation__end__gte=date_time) | Q(occupation__end__isnull=True)
            )
        )


class _CustomManager(models.Manager):

    def get_queryset(self) -> models.QuerySet['Table']:
        return _CustomQuerySet(model=self.model)

    def get_active(self) -> models.QuerySet['Table']:
        return self.get_queryset().get_active()

    def get_by_restaurant_id(self, *, restaurant_id: int) -> models.QuerySet['Table']:
        return self.get_queryset().get_by_restaurant_id(restaurant_id=restaurant_id)

    def get_available_tables(
            self, *, date_time: datetime.datetime
    ) -> models.QuerySet['Table']:
         return self.get_queryset().get_available_tables(date_time=date_time)


class Table(models.Model):
    name = models.CharField(max_length=255)
    seats = models.PositiveIntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    objects = _CustomManager()

    def __str__(self):
        return f'{self.name} ({self.restaurant.name})'

    class Meta:
        ordering = ('name',)
