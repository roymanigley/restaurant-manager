from io import BytesIO

from PIL import Image
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status

from apps.core.models import Restaurant, RestaurantUser, Item, ItemImage


class ItemViewTestCase(TestCase):

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

    def get_dummy_image(self, file_name: str) -> SimpleUploadedFile:
        image = Image.new("RGB", (100, 100), color="blue")
        image_io = BytesIO()
        image.save(image_io, format="JPEG")
        image_io.seek(0)
        return SimpleUploadedFile(
            name=file_name,
            content=image_io.read(),
            content_type='image/jpeg'
        )

    def test_create_for_assigned_restaurant(self):
        # GIVEN
        payload = {
            'name': 'Item 1',
            'description': 'Description for "Item 1"',
            'category': Item.Category.SNAK.value,
            'price': 4.20,
            'restaurant': self.restaurant_assigned.id,
        }
        # WHEN
        response = self.client.post(
            '/staff/items/',
            data=payload,
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )
        response_data = response.json()
        self.assertIsNotNone(response_data['id'], response.content)
        self.assertEqual(response_data['name'], 'Item 1', response.content)
        self.assertEqual(
            response_data['description'], 'Description for "Item 1"', response.content
        )
        self.assertEqual(response_data['category'], Item.Category.SNAK.value, response.content)
        self.assertEqual(response_data['price'], 4.20, response.content)
        self.assertEqual(
            response_data['restaurant'], self.restaurant_assigned.id, response.content
        )
        self.assertIsNone(response_data['image'], response.content)

    def test_create_for_other_restaurant(self):
        # GIVEN
        payload = {
            'name': 'Item 1',
            'description': 'Description for "Item 1"',
            'category': Item.Category.SNAK.value,
            'price': 4.20,
            'restaurant': self.restaurant_other.id
        }
        # WHEN
        response = self.client.post(
            '/staff/items/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.content
        )

    def test_update_for_assigned_restaurant(self):
        # GIVEN
        existing = Item.objects.create(
            name='Item',
            description='Description for "Item"',
            category=Item.Category.SNAK,
            price=4,
            restaurant=self.restaurant_assigned
        )
        payload = {
            'name': 'Item 1',
            'description': 'Description for "Item 1"',
            'category': Item.Category.MAIN.value,
            'price': 4.20,
            'restaurant': self.restaurant_assigned.id,
        }
        # WHEN
        response = self.client.patch(
            f'/staff/items/{existing.id}/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.content
        )
        response_data = response.json()
        self.assertIsNotNone(response_data['id'], response.content)
        self.assertEqual(response_data['name'], 'Item 1', response.content)
        self.assertEqual(
            response_data['description'], 'Description for "Item 1"', response.content
        )
        self.assertEqual(response_data['category'], Item.Category.MAIN.value, response.content)
        self.assertEqual(response_data['price'], 4.20, response.content)
        self.assertEqual(
            response_data['restaurant'], self.restaurant_assigned.id, response.content
        )
        self.assertIsNone(response_data['image'], response.content)

    def test_update_for_assigned_restaurant_with_other_restaurant(self):
        # GIVEN
        existing = Item.objects.create(
            name='Item',
            description='Description for "Item"',
            category=Item.Category.SNAK,
            price=4,
            restaurant=self.restaurant_assigned
        )
        payload = {
            'name': 'Item 1',
            'description': 'Description for "Item 1"',
            'category': Item.Category.MAIN.value,
            'price': 4.20,
            'restaurant': self.restaurant_other.id
        }
        # WHEN
        response = self.client.put(
            f'/staff/items/{existing.id}/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.content
        )

    def test_update_for_other_restaurant(self):
        # GIVEN
        existing = Item.objects.create(
            name='Item',
            description='Description for "Item"',
            category=Item.Category.SNAK,
            price=4,
            restaurant=self.restaurant_assigned
        )
        payload = {
            'name': 'Item 1',
            'description': 'Description for "Item 1"',
            'category': Item.Category.MAIN.value,
            'price': 4.20,
            'restaurant': self.restaurant_other.id
        }
        # WHEN
        response = self.client.put(
            f'/staff/items/{existing.id}/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.content
        )

    def test_update_partial_for_assigned_restaurant(self):
        # GIVEN
        existing = Item.objects.create(
            name='Item',
            description='Description for "Item"',
            category=Item.Category.SNAK,
            price=4,
            restaurant=self.restaurant_assigned
        )
        payload = {
            'name': 'Item 1',
            'category': Item.Category.MAIN.value,
            'price': 4.20,
        }
        # WHEN
        response = self.client.patch(
            f'/staff/items/{existing.id}/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.content
        )
        response_data = response.json()
        self.assertIsNotNone(response_data['id'], response.content)
        self.assertEqual(response_data['name'], 'Item 1', response.content)
        self.assertEqual(
            response_data['description'], 'Description for "Item"', response.content
        )
        self.assertEqual(response_data['category'], Item.Category.MAIN.value, response.content)
        self.assertEqual(response_data['price'], 4.20, response.content)
        self.assertEqual(
            response_data['restaurant'], self.restaurant_assigned.id, response.content
        )
        self.assertIsNone(response_data['image'], response.content)

    def test_update_partial_for_assigned_restaurant_with_other_restaurant(self):
        # GIVEN
        existing = Item.objects.create(
            name='Item',
            description='Description for "Item"',
            category=Item.Category.SNAK,
            price=4,
            restaurant=self.restaurant_assigned
        )
        payload = {
            'restaurant': self.restaurant_other.id
        }
        # WHEN
        response = self.client.patch(
            f'/staff/items/{existing.id}/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.content
        )

    def test_update_partial_for_other_restaurant(self):
        # GIVEN
        existing = Item.objects.create(
            name='Item',
            description='Description for "Item"',
            category=Item.Category.SNAK,
            price=4,
            restaurant=self.restaurant_other
        )
        payload = {
            'restaurant': self.restaurant_other.id
        }
        # WHEN
        response = self.client.patch(
            f'/staff/items/{existing.id}/',
            data=payload,
            content_type='application/json'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.content
        )

    def test_delete_for_assigned_restaurant(self):
        # GIVEN
        existing = Item.objects.create(
            name='Item',
            description='Description for "Item"',
            category=Item.Category.SNAK,
            price=4,
            restaurant=self.restaurant_assigned
        )
        # WHEN
        response = self.client.delete(
            f'/staff/items/{existing.id}/',
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.content
        )

    def test_delete_for_other_restaurant(self):
        # GIVEN
        existing = Item.objects.create(
            name='Item',
            description='Description for "Item"',
            category=Item.Category.SNAK,
            price=4,
            restaurant=self.restaurant_other
        )
        # WHEN
        response = self.client.delete(
            f'/staff/items/{existing.id}/',
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, response.content
        )

    def test_get_with_image_for_assigned_restaurant(self):
        # GIVEN
        existing = Item.objects.create(
            name='Item 1',
            description='Description for "Item 1"',
            category=Item.Category.SNAK,
            price=4,
            restaurant=self.restaurant_assigned
        )
        image_name = 'test-image.jpg'
        image = self.get_dummy_image(image_name)
        ItemImage.objects.create(
            item=existing,
            image=image
        )
        # WHEN
        response = self.client.get(
            f'/staff/items/{existing.id}/',
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.content
        )
        response_data = response.json()
        self.assertIsNotNone(response_data['id'], response.content)
        self.assertEqual(response_data['name'], 'Item 1', response.content)
        self.assertEqual(
            response_data['description'], 'Description for "Item 1"', response.content
        )
        self.assertEqual(response_data['category'], Item.Category.SNAK.value, response.content)
        self.assertEqual(response_data['price'], 4, response.content)
        self.assertEqual(
            response_data['restaurant'], self.restaurant_assigned.id, response.content
        )
        self.assertRegexpMatches(
            response_data['image'],
            r'/item-images/test-image.*\.jpg',
            response.content
        )

    def test_add_image_for_assigned_restaurant(self):
        # GIVEN
        existing = Item.objects.create(
            name='Item 1',
            description='Description for "Item 1"',
            category=Item.Category.SNAK,
            price=4,
            restaurant=self.restaurant_assigned
        )
        image_name = 'test-image.jpg'
        image = self.get_dummy_image(image_name)
        payload = {
            'image': image,
        }
        # WHEN
        response = self.client.post(
            f'/staff/items/{existing.id}/image/',
            data=payload,
            format='multipart'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.content
        )
        response_data = response.json()
        self.assertIsNotNone(response_data['id'], response.content)
        self.assertEqual(response_data['name'], 'Item 1', response.content)
        self.assertEqual(
            response_data['description'], 'Description for "Item 1"', response.content
        )
        self.assertEqual(response_data['category'], Item.Category.SNAK.value, response.content)
        self.assertEqual(response_data['price'], 4, response.content)
        self.assertEqual(
            response_data['restaurant'], self.restaurant_assigned.id, response.content
        )
        self.assertRegexpMatches(
            response_data['image'],
            r'/item-images/test-image.*\.jpg',
            response.content
        )

    def test_update_image_for_assigned_restaurant(self):
        # GIVEN
        existing = Item.objects.create(
            name='Item 1',
            description='Description for "Item 1"',
            category=Item.Category.SNAK,
            price=4,
            restaurant=self.restaurant_assigned
        )
        image_name = 'test-image.jpg'
        image = self.get_dummy_image(image_name)
        ItemImage.objects.create(
            item=existing,
            image=image
        )
        image_name = 'updated-test-image.jpg'
        image = self.get_dummy_image(image_name)
        payload = {
            'image': image,
        }
        # WHEN
        response = self.client.post(
            f'/staff/items/{existing.id}/image/',
            data=payload,
            format='multipart'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.content
        )
        response_data = response.json()
        self.assertIsNotNone(response_data['id'], response.content)
        self.assertEqual(response_data['name'], 'Item 1', response.content)
        self.assertEqual(
            response_data['description'], 'Description for "Item 1"', response.content
        )
        self.assertEqual(response_data['category'], Item.Category.SNAK.value, response.content)
        self.assertEqual(response_data['price'], 4, response.content)
        self.assertEqual(
            response_data['restaurant'], self.restaurant_assigned.id, response.content
        )
        self.assertRegexpMatches(
            response_data['image'],
            r'/item-images/updated-test-image.*\.jpg',
            response.content
        )

    def test_add_image_for_other_restaurant(self):
        # GIVEN
        existing = Item.objects.create(
            name='Item 1',
            description='Description for "Item 1"',
            category=Item.Category.SNAK,
            price=4,
            restaurant=self.restaurant_other
        )
        image_name = 'test-image.jpg'
        image = self.get_dummy_image(image_name)
        payload = {
            'image': image,
        }
        # WHEN
        response = self.client.post(
            f'/staff/items/{existing.id}/image/',
            data=payload,
            format='multipart'
        )
        # THEN
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN, response.content
        )
