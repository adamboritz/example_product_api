from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .test_case_with_fixture_data import TestCaseWithFixtureData


class WhenSendingAGetToAttributeListView(TestCaseWithFixtureData):
    """This class defines the test suite for a GET request to the attributes view"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAGetToAttributeListView, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.get(
            reverse("attributes"),
            format="json"
        )

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)


class WhenSendingAGetToAttributeListViewWithAValidQueryString(TestCaseWithFixtureData):
    """This is to test search behavior with a valid querystring"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAGetToAttributeListViewWithAValidQueryString, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.get(
            reverse("attributes"),
            data={"type": "Color"},
            format="json")

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)

    def test_should_receive_one_attribute(self):
        self.assertEqual(len(self.response.data), 1)


class WhenSendingAGetToAttributeListViewWithAnInvalidQueryString(TestCaseWithFixtureData):
    """This is to test search behavior with an inalid querystring"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAGetToAttributeListViewWithAnInvalidQueryString, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.get(
            reverse("attributes"),
            data={"type2": "Color"},
            format="json")

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)

    def test_should_do_no_filtering(self):
        self.assertEqual(len(self.response.data), 3)


class WhenSendingAPostToAttributeListView(TestCaseWithFixtureData):
    """This class defines the test suite for a POST request to the attributes view"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAPostToAttributeListView, cls).setUpTestData()

        cls.client = APIClient()
        cls.attribute_data = {
            "type": "Color",
            "value": "Black"
        }
        cls.response = cls.client.post(
            reverse("attributes"),
            cls.attribute_data,
            format="json"
        )
        cls.response.render()

    def test_should_receive_a_201_created_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_201_CREATED)

    def test_should_have_an_id_for_created_attribute(self):
        self.assertIn("id", self.response.data)


class WhenSendingAnUnsupportedMethodToAttributeListView(TestCaseWithFixtureData):
    """This class is to show that we expect to receive a bad request when trying to use an unsupported HTTP method"""

    @classmethod
    def setUpTestData(cls):
        super(WhenSendingAnUnsupportedMethodToAttributeListView, cls).setUpTestData()

        cls.client = APIClient()
        cls.response = cls.client.delete(
            reverse("attributes"),
            {
                "type": "color"
            },
            format="json"
        )

    def test_should_receive_a_400_bad_request_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_400_BAD_REQUEST)
