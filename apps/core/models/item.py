from django.db import models

from apps.core.models.restaurant import Restaurant


class _CustomQuerySet(models.QuerySet):

    def get_by_restaurant_id(self, *, restaurant_id: int) -> '_CustomQuerySet[Item]':
        return self.filter(restaurant_id=restaurant_id)

    def get_by_occupation_id(self, *, occupation_id: int) -> '_CustomQuerySet[Item]':
        return self.filter(restaurant__table__occupation__id=occupation_id)

    def get_by_category(self, *, category: str) -> '_CustomQuerySet[Item]':
        return self.filter(category=category)

    def get_active(self) -> '_CustomQuerySet[Item]':
        return self.filter(active=True)


class _CustomManager(models.Manager):

    def get_queryset(self) -> _CustomQuerySet['Item']:
        return _CustomQuerySet(model=self.model)

    def get_active(self) -> _CustomQuerySet['Item']:
        return self.get_queryset().get_active()

    def get_by_restaurant_id(self, *, restaurant_id: int) -> _CustomQuerySet['Item']:
        return self.get_queryset().get_by_restaurant_id(restaurant_id=restaurant_id)

    def get_by_occupation_id(self, *, occupation_id: int) -> _CustomQuerySet['Item']:
        return self.get_queryset().get_by_occupation_id(occupation_id=occupation_id)

    def get_by_category(self, *, category: str) -> _CustomQuerySet['Item']:
        return self.get_queryset().get_by_category(category=category)


class Item(models.Model):
    class Category(models.TextChoices):
        BEVERAGE_NON_ALCOHOLIC = 'BEVERAGE_NON_ALCOHOLIC'
        BEVERAGE_ALCOHOLIC = 'BEVERAGE_ALCOHOLIC'
        SNAK = 'SNACK'
        STARTER = 'STARTER'
        MAIN = 'MAIN'
        DESSERT = 'DESSERT'

    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255, choices=Category.choices, default=None)
    price = models.FloatField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    objects = _CustomManager()

    def __str__(self):
        return f'{self.name} ({self.restaurant.name})'

    class Meta:
        ordering = ('name',)
