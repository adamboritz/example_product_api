from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .test_case_with_fixture_data import TestCaseWithFixtureData


class WhenSendingAGetForAValidAttributeToAttributeDetailView(TestCaseWithFixtureData):
    """This class defines the test suite for a valid GET request to the attribute details view"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAGetForAValidAttributeToAttributeDetailView, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.get(
            reverse("attribute_details", kwargs={'pk': cls.attribute1.id}),
            format="json"
        )

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)

    def test_response_object_should_have_an_id(self):
        self.assertIn("id", self.response.data)


class WhenSendingAGetForAnInvalidAttributeToAttributeDetailView(TestCaseWithFixtureData):
    """This class defines the test suite for an invalid GET request to the attribute details view"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAGetForAnInvalidAttributeToAttributeDetailView, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.get(
            reverse("attribute_details", kwargs={'pk': cls.attribute1.id+2000}),
            format="json"
        )

    def test_should_receive_a_404_not_found_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_404_NOT_FOUND)


class WhenSendingAPostForAValidAttributeToAttributeDetailView(TestCaseWithFixtureData):
    """This class defines the test suite for a valid POST request to the attribute details view"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAPostForAValidAttributeToAttributeDetailView, cls).setUpTestData()

        cls.update_data = {
            "value": "Blue",
            "type": "Color"
        }

        cls.client = APIClient()
        cls.response = cls.client.post(
            reverse("attribute_details", kwargs={'pk': cls.attribute1.id}),
            data=cls.update_data,
            format="json"
        )

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)

    def test_response_object_should_contain_new_color(self):
        self.assertEqual("Blue", self.response.data["value"])


class WhenSendingAPostForAnInvalidAttributeToAttributeDetailView(TestCaseWithFixtureData):
    """This class defines the test suite for an invalid POST request to the attribute details view"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAPostForAnInvalidAttributeToAttributeDetailView, cls).setUpTestData()

        cls.update_data = {"value": "Blue"}

        cls.client = APIClient()
        cls.response = cls.client.post(
            reverse("attribute_details", kwargs={'pk': cls.attribute1.id+2000}),
            data=cls.update_data,
            format="json"
        )

    def test_should_receive_a_404_not_found_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_404_NOT_FOUND)


class WhenSendingAnUnsupportedMethodToAttributeListView(TestCaseWithFixtureData):
    """This class is to show that we expect to receive a bad request when trying to use an unsupported HTTP method"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAnUnsupportedMethodToAttributeListView, cls).setUpTestData()

        cls.update_data = {
            "value": "Blue",
            "type": "Color"
        }

        cls.client = APIClient()
        cls.response = cls.client.put(
            reverse("attribute_details", kwargs={'pk': cls.attribute1.id}),
            data=cls.update_data,
            format="json"
        )

    def test_should_receive_a_400_bad_request_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_400_BAD_REQUEST)
