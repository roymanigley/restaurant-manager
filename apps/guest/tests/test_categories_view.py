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
            f'/guests/categories/{self.occupation_active.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        response_data = response.json()
        self.assertEqual(response_data['count'], len(Item.Category.choices))

    def test_inactive_occupation(self):
        response = self.client.get(
            f'/guests/categories/{self.occupation_inactive.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)
