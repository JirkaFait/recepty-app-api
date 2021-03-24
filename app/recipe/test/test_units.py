from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Units

from recipe.serializers import UnitsSerializer


UNITS_URL = reverse('recipe:units-list')


class PublicUnitsApiTests(TestCase):
    """Testovani jestli je viditelne units API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving units"""
        res = self.client.get(UNITS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUnitsApiTests(TestCase):
    """Test the authorized user units API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_units(self):
        """Test retrieving units"""
        Units.objects.create(user=self.user, name='PL', title='Polevka')
        Units.objects.create(user=self.user, name='g', title='Gram')

        res = self.client.get(UNITS_URL)

        units = Units.objects.all().order_by('-name')
        serializer = UnitsSerializer(units, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that units returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        Units.objects.create(user=user2, name='Kl')
        unit = Units.objects.create(user=self.user, name='Hl')

        res = self.client.get(UNITS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], unit.name)

    def test_create_tag_successful(self):
        """Test creating a new units"""
        payload = {'name': 'CJ', 'title': 'cajovka'}
        self.client.post(UNITS_URL, payload)

        exists = Units.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new units with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(UNITS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

