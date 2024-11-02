from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now
from rest_framework import status

from apps.core.models import Restaurant, Occupation, Table, RestaurantUser, Item


class ItemViewTestCase(TestCase):
    TOTAL_ACTIVE_ITEMS_PER_RESTAURANT = 25
    TOTAL_ACTIVE_SNACK_ITEMS_PER_RESTAURANT = 5
    TOTAL_ACTIVE_MAIN_ITEMS_PER_RESTAURANT = 20

    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='The Prancing Pony'
        )
        self.restaurant_other = Restaurant.objects.create(
            name='Not The Prancing Pony'
        )
        for i in range(self.TOTAL_ACTIVE_ITEMS_PER_RESTAURANT):
            Item.objects.create(
                name=f'Item {i}',
                description=f'Item {i} active',
                category=Item.Category.SNAK if i < self.TOTAL_ACTIVE_SNACK_ITEMS_PER_RESTAURANT else Item.Category.MAIN,
                price=i + 0.5,
                restaurant=self.restaurant
            )
            Item.objects.create(
                name=f'Item {i} inactive',
                description=f'Item {i}',
                category=Item.Category.SNAK if i < self.TOTAL_ACTIVE_SNACK_ITEMS_PER_RESTAURANT else Item.Category.MAIN,
                price=i + 0.5,
                restaurant=self.restaurant,
                active=False
            )
            Item.objects.create(
                name=f'Item {i} active other Restaurant',
                description=f'Item {i}',
                category=Item.Category.SNAK if i < self.TOTAL_ACTIVE_SNACK_ITEMS_PER_RESTAURANT else Item.Category.MAIN,
                price=i + 0.5,
                restaurant=self.restaurant_other
            )
            Item.objects.create(
                name=f'Item {i} inactive other Restaurant',
                description=f'Item {i}',
                category=Item.Category.SNAK if i < self.TOTAL_ACTIVE_SNACK_ITEMS_PER_RESTAURANT else Item.Category.MAIN,
                price=i + 0.5,
                restaurant=self.restaurant_other,
                active=False
            )
        self.waiter = RestaurantUser.objects.create(
            username='Emilio',
            restaurant=self.restaurant
        )
        self.waiter_other_restaurant = RestaurantUser.objects.create(
            username='Adolf',
            restaurant=self.restaurant_other
        )
        self.table = Table.objects.create(
            name='Table 01',
            seats=4,
            restaurant=self.restaurant
        )
        self.active_occupation_start_date = now()

        self.occupation_active = Occupation.objects.create(
            start=self.active_occupation_start_date,
            table=self.table,
            waiter=self.waiter,
        )
        self.occupation_inactive = Occupation.objects.create(
            start=self.active_occupation_start_date - timedelta(hours=1),
            end=self.active_occupation_start_date - timedelta(minutes=1),
            table=self.table,
            waiter=self.waiter,
        )

    def test_active_occupation(self):
        response = self.client.get(
            f'/guests/items/available/{self.occupation_active.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = response.json()
        self.assertEqual(response_data['count'], self.TOTAL_ACTIVE_ITEMS_PER_RESTAURANT)

    def test_active_occupation_snack(self):
        response = self.client.get(
            f'/guests/items/available/{self.occupation_active.id}/{Item.Category.SNAK.value}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = response.json()
        self.assertEqual(response_data['count'], self.TOTAL_ACTIVE_SNACK_ITEMS_PER_RESTAURANT)

    def test_active_occupation_main(self):
        response = self.client.get(
            f'/guests/items/available/{self.occupation_active.id}/{Item.Category.MAIN.value}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = response.json()
        self.assertEqual(response_data['count'], self.TOTAL_ACTIVE_MAIN_ITEMS_PER_RESTAURANT)

    def test_inactive_occupation(self):
        response = self.client.get(
            f'/guests/items/available/{self.occupation_inactive.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)