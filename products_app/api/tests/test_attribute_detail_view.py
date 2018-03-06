from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from api.models import Attribute


class WhenSendingAGetForAValidAttributeToAttributeDetailView(TestCase):
    """This class defines the test suite for a valid GET request to the attribute details view"""

    @classmethod
    def setUpTestData(cls):
        cls.attribute = Attribute(type="Color", value="Red")
        cls.attribute.save()

        cls.client = APIClient()
        cls.response = cls.client.get(
            reverse("attribute_details", kwargs={'pk': cls.attribute.id}),
            format="json"
        )

    @classmethod
    def tearDownClass(cls):
        Attribute.objects.all().delete()

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)

    def test_response_object_should_have_an_id(self):
        self.assertIn(b"id", self.response.content)


class WhenSendingAGetForAnInvalidAttributeToAttributeDetailView(TestCase):
    """This class defines the test suite for an invalid GET request to the attribute details view"""

    @classmethod
    def setUpTestData(cls):
        cls.attribute = Attribute(type="Color", value="Red")
        cls.attribute.save()

        cls.client = APIClient()
        cls.response = cls.client.get(
            reverse("attribute_details", kwargs={'pk': cls.attribute.id+2000}),
            format="json"
        )

    @classmethod
    def tearDownClass(cls):
        Attribute.objects.all().delete()

    def test_should_receive_a_404_not_found_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_404_NOT_FOUND)


class WhenSendingAPostForAValidAttributeToAttributeDetailView(TestCase):
    """This class defines the test suite for a valid POST request to the attribute details view"""

    @classmethod
    def setUpTestData(cls):
        cls.attribute = Attribute(type="Color", value="Red")
        cls.attribute.save()

        cls.update_data = {
            "value": "Blue",
            "type": "Color"
        }

        cls.client = APIClient()
        cls.response = cls.client.post(
            reverse("attribute_details", kwargs={'pk': cls.attribute.id}),
            data=cls.update_data,
            format="json"
        )

    @classmethod
    def tearDownClass(cls):
        Attribute.objects.all().delete()

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)

    def test_response_object_should_contain_new_color(self):
        self.assertIn(b"Blue", self.response.content)


class WhenSendingAPostForAnInvalidAttributeToAttributeDetailView(TestCase):
    """This class defines the test suite for an invalid POST request to the attribute details view"""

    @classmethod
    def setUpTestData(cls):
        cls.attribute = Attribute(type="Color", value="Red")
        cls.attribute.save()

        cls.update_data = {"value": "Blue"}

        cls.client = APIClient()
        cls.response = cls.client.post(
            reverse("attribute_details", kwargs={'pk': cls.attribute.id+2000}),
            data=cls.update_data,
            format="json"
        )

    @classmethod
    def tearDownClass(cls):
        Attribute.objects.all().delete()

    def test_should_receive_a_404_not_found_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_404_NOT_FOUND)


class WhenSendingAnUnsupportedMethodToAttributeListView(TestCase):
    """This class is to show that we expect to receive a bad request when trying to use an unsupported HTTP method"""

    @classmethod
    def setUpTestData(cls):
        cls.attribute = Attribute(type="Color", value="Red")
        cls.attribute.save()

        cls.update_data = {
            "value": "Blue",
            "type": "Color"
        }

        cls.client = APIClient()
        cls.response = cls.client.put(
            reverse("attribute_details", kwargs={'pk': cls.attribute.id}),
            data=cls.update_data,
            format="json"
        )

    def test_should_receive_a_400_bad_request_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_400_BAD_REQUEST)
