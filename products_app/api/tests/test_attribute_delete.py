from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .test_case_with_fixture_data import TestCaseWithFixtureData


class WhenSendingAPostForAValidAttributeToDelete(TestCaseWithFixtureData):
    """This class defines the test suite for a valid POST request to delete an attribute"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAPostForAValidAttributeToDelete, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.post(
            reverse("attribute_delete", kwargs={'pk': cls.attribute1.id}),
            format="json"
        )

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)


class WhenSendingAPostForAnInvalidAttributeToDelete(TestCaseWithFixtureData):
    """This class defines the test suite for an invalid POST request to delete an attribute"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAPostForAnInvalidAttributeToDelete, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.post(
            reverse("attribute_delete", kwargs={'pk': 5000}),
            format="json"
        )

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_404_NOT_FOUND)


class WhenSendingAnUnsupportedMethodToAttributeDeleteView(TestCaseWithFixtureData):
    """This class is to show that we expect to receive a bad request when trying to use an unsupported HTTP method"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAnUnsupportedMethodToAttributeDeleteView, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.put(
            reverse("attribute_delete", kwargs={'pk': cls.attribute1.id}),
            format="json"
        )

    def test_should_receive_a_400_bad_request_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_400_BAD_REQUEST)
