from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from api.models import Product


class WhenSendingAGetForAValidProductToProductDetailView(TestCase):
    """This class defines the test suite for a valid GET request to the product details view"""

    @classmethod
    def setUpTestData(cls):
        cls.product = Product(name="Apple iPhoneX", price=999.99, manufacturer="Apple", product_type="Smartphone")
        cls.product.save()

        cls.client = APIClient()
        cls.response = cls.client.get(
            reverse("product_details", kwargs={'pk': cls.product.id}),
            format="json"
        )

    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)

    def test_response_object_should_have_an_id(self):
        self.assertIn(b"id", self.response.content)


class WhenSendingAGetForAnInvalidProductToProductDetailView(TestCase):
    """This class defines the test suite for an invalid GET request to the product details view"""

    @classmethod
    def setUpTestData(cls):
        cls.product = Product(name="Apple iPhoneX", price=999.99, manufacturer="Apple", product_type="Smartphone")
        cls.product.save()

        cls.client = APIClient()
        cls.response = cls.client.get(
            reverse("product_details", kwargs={'pk': cls.product.id + 2000}),
            format="json"
        )

    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()

    def test_should_receive_a_404_not_found_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_404_NOT_FOUND)


class WhenSendingAPostForAValidAttributeToAttributeDetailView(TestCase):
    """This class defines the test suite for a valid POST request to the product details view"""

    @classmethod
    def setUpTestData(cls):
        cls.product = Product(name="Apple iPhoneX", price=999.99, manufacturer="Apple", product_type="Smartphone")
        cls.product.save()

        cls.update_data = {
            "name": "Apple iPhone X",
            "price": 500.00,
            "manufacturer": "Apple",
            "product_type": "Smartphone",
            "release_date": str(cls.product.release_date)
        }

        cls.client = APIClient()
        cls.response = cls.client.post(
            reverse("product_details", kwargs={'pk': cls.product.id}),
            data=cls.update_data,
            format="json"
        )

    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)

    def test_response_object_should_contain_new_price(self):
        self.assertIn(b"500.00", self.response.content)


class WhenSendingAPostForAnInvalidProductToProductDetailView(TestCase):
    """This class defines the test suite for an invalid POST request to the product details view"""

    @classmethod
    def setUpTestData(cls):
        cls.product = Product(name="Apple iPhoneX", price=999.99, manufacturer="Apple", product_type="Smartphone")
        cls.product.save()

        cls.update_data = {
            "name": "Apple iPhone X",
            "price": 500.00,
            "manufacturer": "Apple",
            "product_type": "Smartphone",
            "release_date": str(cls.product.release_date)
        }

        cls.client = APIClient()
        cls.response = cls.client.post(
            reverse("product_details", kwargs={'pk': cls.product.id + 2000}),
            data=cls.update_data,
            format="json"
        )

    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()

    def test_should_receive_a_404_not_found_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_404_NOT_FOUND)


class WhenSendingAnUnsupportedMethodToProductListView(TestCase):
    """This class is to show that we expect to receive a bad request when trying to use an unsupported HTTP method"""

    @classmethod
    def setUpTestData(cls):
        cls.product = Product(name="Apple iPhoneX", price=999.99, manufacturer="Apple", product_type="Smartphone")
        cls.product.save()

        cls.update_data = {
            "name": "Apple iPhone X",
            "price": 500.00,
            "manufacturer": "Apple",
            "product_type": "Smartphone",
            "release_date": str(cls.product.release_date)
        }

        cls.client = APIClient()
        cls.response = cls.client.put(
            reverse("product_details", kwargs={'pk': cls.product.id}),
            data=cls.update_data,
            format="json"
        )

    def test_should_receive_a_400_bad_request_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_400_BAD_REQUEST)
