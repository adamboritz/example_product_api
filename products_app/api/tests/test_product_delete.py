from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .test_case_setup import TestCaseSetup

class WhenSendingAPostForAValidProductToDelete(TestCaseSetup):
    """This class defines the test suite for a valid POST request to delete a product"""
    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAPostForAValidProductToDelete, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.post(
            reverse("product_delete", kwargs={'pk': cls.product1.id}),
            format="json"
        )

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)


class WhenSendingAPostForAnInvalidProductToDelete(TestCaseSetup):
    """This class defines the test suite for an invalid POST request to delete a product"""
    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAPostForAnInvalidProductToDelete, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.post(
            reverse("product_delete", kwargs={'pk': 5000}),
            format="json"
        )

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_404_NOT_FOUND)


class WhenSendingAnUnsupportedMethodToProductDeleteView(TestCaseSetup):
    """This class is to show that we expect to receive a bad request when trying to use an unsupported HTTP method"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAnUnsupportedMethodToProductDeleteView, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.put(
            reverse("product_delete", kwargs={'pk': cls.product1.id}),
            format="json"
        )

    def test_should_receive_a_400_bad_request_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_400_BAD_REQUEST)
