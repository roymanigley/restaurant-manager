from django.contrib.auth.models import Permission
from django.test import TestCase
from rest_framework import status

from apps.core.models import Restaurant, RestaurantUser


class RestaurantViewTestCase(TestCase):

    def setUp(self):
        self.restaurant_other = Restaurant.objects.create(
            name='The Other Restaurant')
        self.restaurant_assigned = Restaurant.objects.create(
            name='The Prancing Pony')
        self.restaurant_user = RestaurantUser.objects.create(
            username='sam',
            restaurant=self.restaurant_assigned,
        )
        [self.restaurant_user.user_permissions.add(
            p
        ) for p in Permission.objects.all()]
        self.restaurant_user.set_password('password')
        self.restaurant_user.save()
        self.client.login(
            **{'username': 'sam', 'password': 'password'}
        )

    def test_create_new_restaurant(self):
        # GIVEN
        payload = {
            'name': 'Restaurant 1',
        }
        # WHEN
        response = self.client.post(
            '/staff/restaurants/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.content
        )

    def test_update_for_assigned_restaurant(self):
        # GIVEN
        payload = {
            'name': 'Restaurant 1',
        }
        # WHEN
        response = self.client.put(
            f'/staff/restaurants/{self.restaurant_assigned.id}/',
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
            response_data['name'],
            'Restaurant 1',
            response.content
        )

    def test_update_for_other_restaurant(self):
        # GIVEN
        payload = {
            'name': 'Restaurant 1',
        }
        # WHEN
        response = self.client.put(
            f'/staff/restaurants/{self.restaurant_other.id}/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.content
        )

    def test_update_partial_for_assigned_restaurant(self):
        # GIVEN
        payload = {
            'name': 'Restaurant 1',
        }
        # WHEN
        response = self.client.patch(
            f'/staff/restaurants/{self.restaurant_assigned.id}/',
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
            response_data['name'],
            'Restaurant 1',
            response.content
        )

    def test_update_partial_for_other_restaurant(self):
        # GIVEN
        payload = {
            'name': 'Restaurant 1'
        }
        # WHEN
        response = self.client.patch(
            f'/staff/restaurants/{self.restaurant_other.id}/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.content
        )

    def test_delete_for_assigned_restaurant(self):
        # WHEN
        response = self.client.delete(
            f'/staff/restaurants/{self.restaurant_assigned.id}/',
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.content
        )

    def test_delete_for_other_restaurant(self):
        # WHEN
        response = self.client.delete(
            f'/staff/restaurants/{self.restaurant_other.id}/',
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.content
        )
