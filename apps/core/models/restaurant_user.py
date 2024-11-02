from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from apps.core.models.restaurant import Restaurant


class _CustomQuerySet(models.QuerySet):

    def get_active(self) -> models.QuerySet['RestaurantUser']:
        return self.filter(active=True)

    def get_by_restaurant_id(self, *, restaurant_id: int) -> models.QuerySet['RestaurantUser']:
        return self.filter(restaurant_id=restaurant_id)


class _CustomManager(UserManager):

    def get_queryset(self) -> models.QuerySet['RestaurantUser']:
        return _CustomQuerySet(model=self.model)

    def get_active(self) -> models.QuerySet['RestaurantUser']:
        return self.get_queryset().get_active()

    def get_by_restaurant_id(self, *, restaurant_id: int) -> models.QuerySet['RestaurantUser']:
        return self.get_queryset().get_by_restaurant_id(restaurant_id=restaurant_id)


class RestaurantUser(AbstractUser):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    objects = _CustomManager()

    def __str__(self):
        return f'{self.username} ({self.restaurant.name})'
