from django.contrib.auth.models import Permission
from django.test import TestCase
from rest_framework import status

from apps.core.models import Restaurant, RestaurantUser


class RestaurantUserViewTestCase(TestCase):

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

    # def test_create_for_assigned_restaurant(self):
    #     # GIVEN
    #     payload = {
    #         'username': 'TestRestaurantUser',
    #         'first_name': 'Alberto',
    #         'last_name': 'Sudo',
    #         'password': 'top-secret',
    #         'restaurant': self.restaurant_assigned.id
    #     }
    #     # WHEN
    #     response = self.client.post(
    #         '/staff/restaurant-users/',
    #         data=payload,
    #         content_type='application/json'
    #     )
    #     # THEN
    #     self.assertEqual(
    #         response.status_code, status.HTTP_201_CREATED, response.content
    #     )
    #     response_data = response.json()
    #     self.assertIsNotNone(response_data['id'], response.content)
    #     self.assertEqual(
    #         response_data['username'],
    #         'TestRestaurantUser',
    #         response.content
    #     )
    #     self.assertEqual(
    #         response_data['restaurant'], self.restaurant_assigned.id, response.content
    #     )
    #
    # def test_create_for_other_restaurant(self):
    #     # GIVEN
    #     payload = {
    #         'username': 'TestRestaurantUser',
    #         'first_name': 'Alberto',
    #         'last_name': 'Sudo',
    #         'password': 'top-secret',
    #         'restaurant': self.restaurant_other.id
    #     }
    #     # WHEN
    #     response = self.client.post(
    #         '/staff/restaurant-users/',
    #         data=payload,
    #         content_type='application/json'
    #     )
    #     # THEN
    #     self.assertEqual(
    #         response.status_code, status.HTTP_403_FORBIDDEN, response.content
    #     )
    #
    # def test_update_for_assigned_restaurant(self):
    #     # GIVEN
    #     existing = RestaurantUser.objects.create(
    #         username='RestaurantUser',
    #         password='1234',
    #         restaurant=self.restaurant_assigned
    #     )
    #     payload = {
    #         'username': 'TestRestaurantUser',
    #         'first_name': 'Alberto',
    #         'last_name': 'Sudo',
    #         'password': 'top-secret',
    #         'restaurant': self.restaurant_assigned.id
    #     }
    #     # WHEN
    #     response = self.client.put(
    #         f'/staff/restaurant-users/{existing.id}/',
    #         data=payload,
    #         content_type='application/json'
    #     )
    #     # THEN
    #     self.assertEqual(
    #         response.status_code, status.HTTP_200_OK, response.content
    #     )
    #     response_data = response.json()
    #     self.assertIsNotNone(response_data['id'], response.content)
    #     self.assertEqual(
    #         response_data['username'],
    #         'TestRestaurantUser',
    #         response.content
    #     )
    #     self.assertEqual(
    #         response_data['restaurant'], self.restaurant_assigned.id, response.content
    #     )
    #
    # def test_update_for_assigned_restaurant_with_other_restaurant(self):
    #     # GIVEN
    #     existing = RestaurantUser.objects.create(
    #         username='RestaurantUser',
    #         password='1234',
    #         restaurant=self.restaurant_assigned
    #     )
    #     payload = {
    #         'username': 'TestRestaurantUser',
    #         'first_name': 'Alberto',
    #         'last_name': 'Sudo',
    #         'password': 'top-secret',
    #         'restaurant': self.restaurant_other.id
    #     }
    #     # WHEN
    #     response = self.client.put(
    #         f'/staff/restaurant-users/{existing.id}/',
    #         data=payload,
    #         content_type='application/json'
    #     )
    #     # THEN
    #     self.assertEqual(
    #         response.status_code, status.HTTP_403_FORBIDDEN, response.content
    #     )
    #
    # def test_update_for_other_restaurant(self):
    #     # GIVEN
    #     existing = RestaurantUser.objects.create(
    #         username='RestaurantUser',
    #         password='1234',
    #         restaurant=self.restaurant_other
    #     )
    #     payload = {
    #         'username': 'TestRestaurantUser',
    #         'first_name': 'Alberto',
    #         'last_name': 'Sudo',
    #         'password': 'top-secret',
    #         'restaurant': self.restaurant_other.id
    #     }
    #     # WHEN
    #     response = self.client.put(
    #         f'/staff/restaurant-users/{existing.id}/',
    #         data=payload,
    #         content_type='application/json'
    #     )
    #     # THEN
    #     self.assertEqual(
    #         response.status_code, status.HTTP_403_FORBIDDEN, response.content
    #     )
    #
    # def test_update_partial_for_assigned_restaurant(self):
    #     # GIVEN
    #     existing = RestaurantUser.objects.create(
    #         username='RestaurantUser',
    #         password='1234',
    #         restaurant=self.restaurant_assigned
    #     )
    #     payload = {
    #         'username': 'TestRestaurantUser',
    #     }
    #     # WHEN
    #     response = self.client.patch(
    #         f'/staff/restaurant-users/{existing.id}/',
    #         data=payload,
    #         content_type='application/json'
    #     )
    #     # THEN
    #     self.assertEqual(
    #         response.status_code, status.HTTP_200_OK, response.content
    #     )
    #     response_data = response.json()
    #     self.assertIsNotNone(response_data['id'], response.content)
    #     self.assertEqual(
    #         response_data['username'],
    #         'TestRestaurantUser',
    #         response.content
    #     )
    #     self.assertEqual(
    #         response_data['restaurant'], self.restaurant_assigned.id, response.content
    #     )
    #
    # def test_update_partial_for_assigned_restaurant_with_other_restaurant(self):
    #     # GIVEN
    #     existing = RestaurantUser.objects.create(
    #         username='RestaurantUser',
    #         password='1234',
    #         restaurant=self.restaurant_assigned
    #     )
    #     payload = {
    #         'restaurant': self.restaurant_other.id
    #     }
    #     # WHEN
    #     response = self.client.patch(
    #         f'/staff/restaurant-users/{existing.id}/',
    #         data=payload,
    #         content_type='application/json'
    #     )
    #     # THEN
    #     self.assertEqual(
    #         response.status_code, status.HTTP_403_FORBIDDEN, response.content
    #     )
    #
    # def test_update_partial_for_other_restaurant(self):
    #     # GIVEN
    #     existing = RestaurantUser.objects.create(
    #         username='RestaurantUser',
    #         password='1234',
    #         restaurant=self.restaurant_other
    #     )
    #     payload = {
    #         'restaurant': self.restaurant_other.id
    #     }
    #     # WHEN
    #     response = self.client.patch(
    #         f'/staff/restaurant-users/{existing.id}/',
    #         data=payload,
    #         content_type='application/json'
    #     )
    #     # THEN
    #     self.assertEqual(
    #         response.status_code, status.HTTP_403_FORBIDDEN, response.content
    #     )
    #
    # def test_delete_for_assigned_restaurant(self):
    #     # GIVEN
    #     existing = RestaurantUser.objects.create(
    #         username='RestaurantUser',
    #         password='1234',
    #         restaurant=self.restaurant_assigned
    #     )
    #     # WHEN
    #     response = self.client.delete(
    #         f'/staff/restaurant-users/{existing.id}/',
    #     )
    #     # THEN
    #     self.assertEqual(
    #         response.status_code, status.HTTP_204_NO_CONTENT, response.content
    #     )
    #
    # def test_delete_for_other_restaurant(self):
    #     # GIVEN
    #     existing = RestaurantUser.objects.create(
    #         username='RestaurantUser',
    #         password='1234',
    #         restaurant=self.restaurant_other
    #     )
    #     # WHEN
    #     response = self.client.delete(
    #         f'/staff/restaurant-users/{existing.id}/',
    #     )
    #     # THEN
    #     self.assertEqual(
    #         response.status_code, status.HTTP_404_NOT_FOUND, response.content
    #     )

    def test_get_current_user(self):
        # WHEN
        response = self.client.get(
            f'/staff/restaurant-users/me/',
        )
        # THEN
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(
            response_data['username'],
            self.restaurant_user.username,
            response.content
        )
        self.assertEqual(
            response_data['restaurant'], self.restaurant_assigned.id, response.content
        )
        self.assertEqual(
            response_data['restaurant_name'], self.restaurant_assigned.name, response.content
        )
        self.assertTrue(
            len(response_data['permissions']) > 0,
            response.content
        )

    def test_set_valid_password(self):
        # GIVEN
        payloads = [
            {
                'password_one': 'Server4$',
                'password_two': 'Server4$',
            },
            {
                'password_one': 'fdsafadsff',
                'password_two': 'fdsafadsff',
            },
        ]
        # WHEN
        for payload in payloads:
            response = self.client.put(
                f'/staff/restaurant-users/me/password/',
                data=payload,
                content_type='application/json'
            )
            # THEN
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)
    
    def test_set_invalid_password(self):
        # GIVEN
        payloads = [
            {
                # to short
                'password_one': 'aa',
                'password_two': 'aa',
            },
            {
                # only numeric
                'password_one': '1234567890',
                'password_two': '1234567890',
            },
            {
                # to common
                'password_one': 'password',
                'password_two': 'password',
            },
        ]
        # WHEN
        for payload in payloads:
            response = self.client.put(
                f'/staff/restaurant-users/me/password/',
                data=payload,
                content_type='application/json'
            )
            # THEN
            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
                f'password: {payload["password_one"]} - {response.content}'
            )
