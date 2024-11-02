from django.contrib.auth.models import Permission
from django.test import TestCase
from django.utils.timezone import now
from rest_framework import status

from apps.core.models import Restaurant, RestaurantUser, Occupation, Order, Table, Item


class OrderViewTestCase(TestCase):

    def setUp(self):
        self.restaurant_other = Restaurant.objects.create(
            name='The Other Restaurant')
        self.table_other = Table.objects.create(
            name='The Other Restaurant\'s table 1',
            seats=4,
            restaurant=self.restaurant_other
        )
        self.restaurant_assigned = Restaurant.objects.create(
            name='The Prancing Pony')
        self.table_assigned = Table.objects.create(
            name='The Prancing Pony\'s table 1',
            seats=4,
            restaurant=self.restaurant_assigned
        )
        self.restaurant_user = RestaurantUser.objects.create(
            username='sam',
            restaurant=self.restaurant_assigned,
        )
        self.occupation_other = Occupation.objects.create(
            start=now(),
            table=self.table_other,
            waiter=self.restaurant_user
        )
        self.occupation_assigned = Occupation.objects.create(
            start=now(),
            table=self.table_assigned,
            waiter=self.restaurant_user
        )
        self.item_assigned = Item.objects.create(
            name='dummy item',
            description='lorem ipsum',
            category=Item.Category.SNAK,
            price=5,
            restaurant=self.restaurant_assigned
        )
        self.item_other = Item.objects.create(
            name='dummy item',
            description='lorem ipsum',
            category=Item.Category.SNAK,
            price=5,
            restaurant=self.restaurant_other
        )
        [self.restaurant_user.user_permissions.add(
            p
        ) for p in Permission.objects.all()]
        self.restaurant_user.set_password('password')
        self.restaurant_user.save()
        self.client.login(
            **{'username': 'sam', 'password': 'password'}
        )

    def test_create_for_assigned_restaurant(self):
        # GIVEN
        payload = {
            'state': str(Order.State.OPEN),
            'amount': 1,
            'price_per_item': 5,
            'occupation': self.occupation_assigned.id,
            'item': self.item_assigned.id
        }
        # WHEN
        response = self.client.post(
            '/staff/orders/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )
        response_data = response.json()
        self.assertIsNotNone(response_data['id'], response.content)
        self.assertEqual(
            response_data['state'],
            Order.State.OPEN.value,
            response.content
        )
        self.assertEqual(
            response_data['amount'],
            1,
            response.content
        )
        self.assertEqual(
            response_data['price_per_item'],
            5,
            response.content
        )
        self.assertEqual(
            response_data['occupation'],
            str(self.occupation_assigned.id),
            response.content
        )
        self.assertEqual(
            response_data['item'],
            self.item_assigned.id,
            response.content
        )

    def test_create_for_other_restaurant(self):
        # GIVEN
        payloads = [
            {
                'state': str(Order.State.OPEN),
                'amount': 1,
                'price_per_item': 5,
                'occupation': self.occupation_other.id,
                'item': self.item_assigned.id
            },
            {
                'state': str(Order.State.OPEN),
                'amount': 1,
                'price_per_item': 5,
                'occupation': self.occupation_assigned.id,
                'item': self.item_other.id
            }
        ]
        # WHEN
        for payload in payloads:
            response = self.client.post(
                '/staff/orders/',
                data=payload,
                content_type='application/json'
            )
            # THEN
            self.assertEqual(
                response.status_code, status.HTTP_403_FORBIDDEN, response.content
            )

    def test_update_for_assigned_restaurant(self):
        # GIVEN
        existing = Order.objects.create(
            state=Order.State.OPEN,
            amount=1,
            price_per_item=5,
            occupation=self.occupation_assigned,
            item=self.item_assigned
        )
        payload = {
            'state': str(Order.State.COMPETED),
            'amount': 2,
            'price_per_item': 4,
            'occupation': self.occupation_assigned.id,
            'item': self.item_assigned.id
        }
        # WHEN
        response = self.client.put(
            f'/staff/orders/{existing.id}/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.content
        )
        response_data = response.json()
        self.assertIsNotNone(response_data['id'], response.content)
        self.assertEqual(
            response_data['state'],
            Order.State.COMPETED.value,
            response.content
        )
        self.assertEqual(
            response_data['amount'],
            2,
            response.content
        )
        self.assertEqual(
            response_data['price_per_item'],
            4,
            response.content
        )
        self.assertEqual(
            response_data['occupation'],
            str(self.occupation_assigned.id),
            response.content
        )
        self.assertEqual(
            response_data['item'],
            self.item_assigned.id,
            response.content
        )

    def test_update_for_assigned_restaurant_with_other_restaurant(self):
        # GIVEN
        existing = Order.objects.create(
            state=Order.State.OPEN,
            amount=1,
            price_per_item=5,
            occupation=self.occupation_assigned,
            item=self.item_assigned
        )
        payloads = [
            {
                'state': str(Order.State.COMPETED),
                'amount': 2,
                'price_per_item': 4,
                'occupation': self.occupation_other.id,
                'item': self.item_assigned.id
            },
            {
                'state': str(Order.State.COMPETED),
                'amount': 2,
                'price_per_item': 4,
                'occupation': self.occupation_assigned.id,
                'item': self.item_other.id
            }
        ]
        # WHEN
        for payload in payloads:
            response = self.client.put(
                f'/staff/orders/{existing.id}/',
                data=payload,
                content_type='application/json'
            )
            # THEN
            self.assertEqual(
                response.status_code, status.HTTP_403_FORBIDDEN, response.content
            )

    def test_update_for_other_restaurant(self):
        # GIVEN
        existing = Order.objects.create(
            state=Order.State.OPEN,
            amount=1,
            price_per_item=5,
            occupation=self.occupation_other,
            item=self.item_other
        )
        payload = {
            'state': str(Order.State.COMPETED),
            'amount': 2,
            'price_per_item': 4,
            'occupation': self.occupation_assigned.id,
            'item': self.item_assigned.id
        }
        # WHEN
        response = self.client.put(
            f'/staff/orders/{existing.id}/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.content
        )

    def test_update_partial_for_assigned_restaurant(self):
        # GIVEN
        existing = Order.objects.create(
            state=Order.State.OPEN,
            amount=1,
            price_per_item=5,
            occupation=self.occupation_assigned,
            item=self.item_assigned
        )
        payload = {
            'state': Order.State.COMPETED,
        }

        # WHEN
        response = self.client.patch(
            f'/staff/orders/{existing.id}/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.content
        )
        response_data = response.json()
        self.assertIsNotNone(response_data['id'], response.content)
        self.assertEqual(
            response_data['state'],
            Order.State.COMPETED.value,
            response.content
        )
        self.assertEqual(
            response_data['amount'],
            1,
            response.content
        )
        self.assertEqual(
            response_data['price_per_item'],
            5,
            response.content
        )
        self.assertEqual(
            response_data['occupation'],
            str(self.occupation_assigned.id),
            response.content
        )
        self.assertEqual(
            response_data['item'],
            self.item_assigned.id,
            response.content
        )

    def test_update_partial_for_assigned_restaurant_with_other_restaurant(self):
        # GIVEN
        existing = Order.objects.create(
            state=Order.State.OPEN,
            amount=1,
            price_per_item=5,
            occupation=self.occupation_assigned,
            item=self.item_assigned
        )
        payloads = [
            {
                'occupation': self.occupation_other.id,
            },
            {
                'item': self.item_other.id,
            }
        ]
        # WHEN
        for payload in payloads:
            response = self.client.patch(
                f'/staff/orders/{existing.id}/',
                data=payload,
                content_type='application/json'
            )
            # THEN
            self.assertEqual(
                response.status_code, status.HTTP_403_FORBIDDEN, response.content
            )

    def test_update_partial_for_other_restaurant(self):
        # GIVEN
        existing = Order.objects.create(
            state=Order.State.OPEN,
            amount=1,
            price_per_item=5,
            occupation=self.occupation_other,
            item=self.item_other
        )
        payload = {
            'state': Order.State.COMPETED,
            'occupation': self.occupation_assigned.id,
            'item': self.item_assigned.id,
        }
        # WHEN
        response = self.client.patch(
            f'/staff/orders/{existing.id}/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.content
        )

    def test_delete_for_assigned_restaurant(self):
        # GIVEN
        existing = Order.objects.create(
            state=Order.State.OPEN,
            amount=1,
            price_per_item=5,
            occupation=self.occupation_assigned,
            item=self.item_assigned
        )
        # WHEN
        response = self.client.delete(
            f'/staff/orders/{existing.id}/',
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.content
        )

    def test_delete_for_other_restaurant(self):
        # GIVEN
        existing = Order.objects.create(
            state=Order.State.OPEN,
            amount=1,
            price_per_item=5,
            occupation=self.occupation_other,
            item=self.item_other
        )
        # WHEN
        response = self.client.delete(
            f'/staff/orders/{existing.id}/',
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.content
        )
