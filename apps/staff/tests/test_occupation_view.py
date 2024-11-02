import datetime

from django.contrib.auth.models import Permission
from django.test import TestCase
from rest_framework import status

from apps.core.models import Restaurant, RestaurantUser, Occupation, Table


class OccupationViewTestCase(TestCase):

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
        self.restaurant_user_other = RestaurantUser.objects.create(
            username='not_sam',
            restaurant=self.restaurant_other,
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
        start_date_iso = datetime.datetime.now().isoformat() + 'Z'
        payload = {
            'start': start_date_iso,
            'table': self.table_assigned.id,
            'waiter': self.restaurant_user.id,
        }
        # WHEN
        response = self.client.post(
            '/staff/occupations/',
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
            response_data['start'],
            start_date_iso,
            response.content
        )
        self.assertEqual(
            response_data['table'],
            self.table_assigned.id,
            response.content
        )

    def test_create_for_other_restaurant(self):
        # GIVEN
        start_date_iso = datetime.datetime.now().isoformat() + 'Z'
        payloads = [
            {
                'start': start_date_iso,
                'table': self.table_other.id,
                'waiter': self.restaurant_user.id,
            },
            {
                'start': start_date_iso,
                'table': self.table_assigned.id,
                'waiter': self.restaurant_user_other.id,
            }

        ]
        # WHEN
        for payload in payloads:
            response = self.client.post(
                '/staff/occupations/',
                data=payload,
                content_type='application/json'
            )
            # THEN
            self.assertEqual(
                response.status_code, status.HTTP_403_FORBIDDEN, response.content
            )

    def test_update_for_assigned_restaurant(self):
        # GIVEN
        initial_start_date_iso = (
                                         datetime.datetime.now() + datetime.timedelta(hours=-1)
                                 ).isoformat() + 'Z'
        existing = Occupation.objects.create(
            start=initial_start_date_iso,
            table=self.table_assigned,
            waiter=self.restaurant_user,
        )
        updated_start_date_iso = datetime.datetime.now().isoformat() + 'Z'
        payload = {
            'start': updated_start_date_iso,
            'table': self.table_assigned.id,
            'waiter': self.restaurant_user.id,
        }
        # WHEN
        response = self.client.put(
            f'/staff/occupations/{existing.id}/',
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
            response_data['start'],
            updated_start_date_iso,
            response.content
        )
        self.assertEqual(
            response_data['table'],
            self.table_assigned.id,
            response.content
        )

    def test_update_for_assigned_restaurant_with_other_restaurant(self):
        # GIVEN
        initial_start_date_iso = (
                                         datetime.datetime.now() + datetime.timedelta(hours=-1)
                                 ).isoformat() + 'Z'
        existing = Occupation.objects.create(
            start=initial_start_date_iso,
            table=self.table_assigned,
            waiter=self.restaurant_user,
        )
        updated_start_date_iso = datetime.datetime.now().isoformat() + 'Z'
        payloads = [
            {
                'start': updated_start_date_iso,
                'table': self.table_other.id,
                'waiter': self.restaurant_user.id,
            },
            {
                'start': updated_start_date_iso,
                'table': self.table_assigned.id,
                'waiter': self.restaurant_user_other.id,
            }

        ]
        # WHEN
        for payload in payloads:
            response = self.client.put(
                f'/staff/occupations/{existing.id}/',
                data=payload,
                content_type='application/json'
            )
            # THEN
            self.assertEqual(
                response.status_code, status.HTTP_403_FORBIDDEN, response.content
            )

    def test_update_for_other_restaurant(self):
        # GIVEN
        initial_start_date_iso = (
                                         datetime.datetime.now() + datetime.timedelta(hours=-1)
                                 ).isoformat() + 'Z'
        existing = Occupation.objects.create(
            start=initial_start_date_iso,
            table=self.table_assigned,
            waiter=self.restaurant_user,
        )
        updated_start_date_iso = datetime.datetime.now().isoformat() + 'Z'
        payload = {
            'start': updated_start_date_iso,
            'table': self.table_other.id,
            'waiter': self.restaurant_user.id,
        }
        # WHEN
        response = self.client.put(
            f'/staff/occupations/{existing.id}/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.content
        )

    def test_update_partial_for_assigned_restaurant(self):
        # GIVEN
        start_date_iso = (
                                 datetime.datetime.now() + datetime.timedelta(hours=-1)
                         ).isoformat() + 'Z'
        existing = Occupation.objects.create(
            start=start_date_iso,
            table=self.table_assigned,
            waiter=self.restaurant_user,
        )
        end_date_iso = datetime.datetime.now().isoformat() + 'Z'
        payload = {
            'end': end_date_iso,
        }

        # WHEN
        response = self.client.patch(
            f'/staff/occupations/{existing.id}/',
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
            response_data['start'],
            start_date_iso,
            response.content
        )
        self.assertEqual(
            response_data['end'],
            end_date_iso,
            response.content
        )
        self.assertEqual(
            response_data['table'],
            self.table_assigned.id,
            response.content
        )

    def test_update_partial_for_assigned_restaurant_with_other_restaurant(self):
        # GIVEN
        start_date_iso = (
                                 datetime.datetime.now() + datetime.timedelta(hours=-1)
                         ).isoformat() + 'Z'
        existing = Occupation.objects.create(
            start=start_date_iso,
            table=self.table_assigned,
            waiter=self.restaurant_user,
        )
        payloads = [
            {
                'table': self.table_other.id,
            },
            {
                'waiter': self.restaurant_user_other.id,
            }
        ]
        # WHEN
        for payload in payloads:
            response = self.client.patch(
                f'/staff/occupations/{existing.id}/',
                data=payload,
                content_type='application/json'
            )
            # THEN
            self.assertEqual(
                response.status_code, status.HTTP_403_FORBIDDEN, response.content
            )

    def test_update_partial_for_other_restaurant(self):
        # GIVEN
        start_date_iso = (
                                 datetime.datetime.now() + datetime.timedelta(hours=-1)
                         ).isoformat() + 'Z'
        existing = Occupation.objects.create(
            start=start_date_iso,
            table=self.table_other,
            waiter=self.restaurant_user,
        )
        payload = {
            'table': self.table_other.id,
        }
        # WHEN
        response = self.client.patch(
            f'/staff/occupations/{existing.id}/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.content
        )

    def test_delete_for_assigned_restaurant(self):
        # GIVEN
        start_date_iso = (
                                 datetime.datetime.now() + datetime.timedelta(hours=-1)
                         ).isoformat() + 'Z'
        existing = Occupation.objects.create(
            start=start_date_iso,
            table=self.table_assigned,
            waiter=self.restaurant_user,
        )
        # WHEN
        response = self.client.delete(
            f'/staff/occupations/{existing.id}/',
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.content
        )

    def test_delete_for_other_restaurant(self):
        # GIVEN
        start_date_iso = (
                                 datetime.datetime.now() + datetime.timedelta(hours=-1)
                         ).isoformat() + 'Z'
        existing = Occupation.objects.create(
            start=start_date_iso,
            table=self.table_other,
            waiter=self.restaurant_user,
        )
        # WHEN
        response = self.client.delete(
            f'/staff/occupations/{existing.id}/',
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.content
        )
