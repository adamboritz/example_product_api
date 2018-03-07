from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .test_case_with_fixture_data import TestCaseWithFixtureData


class WhenSendingAGetForAValidProductToProductDetailView(TestCaseWithFixtureData):
    """This class defines the test suite for a valid GET request to the product details view"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAGetForAValidProductToProductDetailView, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.get(
            reverse("product_details", kwargs={'pk': cls.product1.id}),
            format="json"
        )

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)

    def test_response_object_should_have_an_id(self):
        self.assertIn("id", self.response.data)


class WhenSendingAGetForAnInvalidProductToProductDetailView(TestCaseWithFixtureData):
    """This class defines the test suite for an invalid GET request to the product details view"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAGetForAnInvalidProductToProductDetailView, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.get(
            reverse("product_details", kwargs={'pk': cls.product1.id + 2000}),
            format="json"
        )

    def test_should_receive_a_404_not_found_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_404_NOT_FOUND)


class WhenSendingAPostForAValidAttributeToAttributeDetailView(TestCaseWithFixtureData):
    """This class defines the test suite for a valid POST request to the product details view"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAPostForAValidAttributeToAttributeDetailView, cls).setUpTestData()

        cls.update_data = {
            "name": "Apple iPhone X",
            "price": 500.00,
            "manufacturer": "Apple",
            "product_type": "Smartphone",
            "release_date": str(cls.product1.release_date)
        }

        cls.client = APIClient()
        cls.response = cls.client.post(
            reverse("product_details", kwargs={'pk': cls.product1.id}),
            data=cls.update_data,
            format="json"
        )

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)

    def test_response_object_should_contain_new_price(self):
        self.assertEqual("500.00", self.response.data["price"])


class WhenSendingAPostForAnInvalidProductToProductDetailView(TestCaseWithFixtureData):
    """This class defines the test suite for an invalid POST request to the product details view"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAPostForAnInvalidProductToProductDetailView, cls).setUpTestData()

        cls.update_data = {
            "name": "Apple iPhone X",
            "price": 500.00,
            "manufacturer": "Apple",
            "product_type": "Smartphone",
            "release_date": str(cls.product1.release_date)
        }

        cls.client = APIClient()
        cls.response = cls.client.post(
            reverse("product_details", kwargs={'pk': cls.product1.id + 2000}),
            data=cls.update_data,
            format="json"
        )

    def test_should_receive_a_404_not_found_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_404_NOT_FOUND)


class WhenSendingAnUnsupportedMethodToProductListView(TestCaseWithFixtureData):
    """This class is to show that we expect to receive a bad request when trying to use an unsupported HTTP method"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAnUnsupportedMethodToProductListView, cls).setUpTestData()

        cls.update_data = {
            "name": "Apple iPhone X",
            "price": 500.00,
            "manufacturer": "Apple",
            "product_type": "Smartphone",
            "release_date": str(cls.product1.release_date)
        }

        cls.client = APIClient()
        cls.response = cls.client.put(
            reverse("product_details", kwargs={'pk': cls.product1.id}),
            data=cls.update_data,
            format="json"
        )

    def test_should_receive_a_400_bad_request_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_400_BAD_REQUEST)
