from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .test_case_with_fixture_data import TestCaseWithFixtureData


class WhenSendingAGetToProductListView(TestCaseWithFixtureData):
    """This class defines the test suite for a GET request to the attributes view"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAGetToProductListView, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.get(
            reverse("products"),
            format="json"
        )

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)


class WhenSendingAGetToProductListViewWithAValidQueryString(TestCaseWithFixtureData):
    """This is to test search behavior with a valid querystring"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAGetToProductListViewWithAValidQueryString, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.get(
            reverse("products"),
            data={"name": "iWatch"},
            format="json")

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)

    def test_should_receive_one_attribute(self):
        self.assertEqual(len(self.response.data), 1)


class WhenSendingAGetToProductListViewWithAnInvalidQueryString(TestCaseWithFixtureData):
    """This is to test search behavior with an inalid querystring"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAGetToProductListViewWithAnInvalidQueryString, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.get(
            reverse("products"),
            data={"type2": "Color"},
            format="json")

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)

    def test_should_do_no_filtering(self):
        self.assertEqual(len(self.response.data), 3)


class WhenSendingAPostToProductListView(TestCaseWithFixtureData):
    """This class defines the test suite for a POST request to the attributes view"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAPostToProductListView, cls).setUpTestData()

        cls.client = APIClient()
        cls.attribute_data = {
            "name": "Color",
            "price": 500.00,
            "manufacturer": "Black",
            "product_type": "Anonymous"
        }
        cls.response = cls.client.post(
            reverse("products"),
            cls.attribute_data,
            format="json"
        )
        cls.response.render()

    def test_should_receive_a_201_created_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_201_CREATED)

    def test_should_have_an_id_for_created_attribute(self):
        self.assertIn(b"id", self.response.content)


class WhenSendingAnUnsupportedMethodToProductsListView(TestCaseWithFixtureData):
    """This class is to show that we expect to receive a bad request when trying to use an unsupported HTTP method"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAnUnsupportedMethodToProductsListView, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.delete(
            reverse("products"),
            {
                "name": "color"
            },
            format="json"
        )

    def test_should_receive_a_400_bad_request_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_400_BAD_REQUEST)
