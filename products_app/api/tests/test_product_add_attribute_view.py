from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .test_case_with_fixture_data import TestCaseWithFixtureData


class WhenSendingAPostForAValidAttributeToProductAddAttributeView(TestCaseWithFixtureData):
    """This class defines the test suite for a valid POST request to the product add attribute view"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAPostForAValidAttributeToProductAddAttributeView, cls).setUpTestData()

        cls.update_data = {
            "attribute_id": cls.attribute1.id
        }

        cls.client = APIClient()
        cls.response = cls.client.post(
            reverse("product_add_attribute", kwargs={'pk': cls.product1.id}),
            data=cls.update_data,
            format="json"
        )

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)

    def test_response_object_should_contain_added_attribute(self):
        self.assertIsNotNone(
            next(attrib for attrib in self.response.data["attributes"] if attrib['id'] == self.attribute1.id))


class WhenSendingAPostForAnInvalidProductToProductAddAttributeView(TestCaseWithFixtureData):
    """This class defines the test suite for an invalid POST request to the product add attribute view"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAPostForAnInvalidProductToProductAddAttributeView, cls).setUpTestData()

        cls.update_data = {
            "attribute_id": cls.attribute1.id
        }

        cls.client = APIClient()
        cls.response = cls.client.post(
            reverse("product_add_attribute", kwargs={'pk': cls.product1.id + 2000}),
            data=cls.update_data,
            format="json"
        )

    def test_should_receive_a_404_not_found_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_404_NOT_FOUND)


class WhenSendingAnUnsupportedMethodToProductAddAttributeView(TestCaseWithFixtureData):
    """This class is to show that we expect to receive a bad request when trying to use an unsupported HTTP method"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAnUnsupportedMethodToProductAddAttributeView, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.get(
            reverse("product_add_attribute", kwargs={'pk': cls.product1.id}),
            format="json"
        )

    def test_should_receive_a_400_bad_request_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_400_BAD_REQUEST)
