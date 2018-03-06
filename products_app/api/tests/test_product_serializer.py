from django.test import TestCase

from api.models import Attribute
from api.models import Product
from api.serializers import ProductSerializer


class WhenSerializingAProductTests(TestCase):
    """This class defines the test suite for serializing a product."""

    @classmethod
    def setUpTestData(cls):
        cls.product = Product(name="Apple iPhoneX", price=999.99, manufacturer="Apple", product_type="Smartphone")
        cls.product.save()
        cls.serializer = ProductSerializer(instance=cls.product)

    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()
        Attribute.objects.all().delete()

    # As there is no custom behavior being specified, just need to test to ensure the one thing that we control is
    # being tested
    def test_keys_should_match_supplied_list(self):
        expected_keys = ['id', 'name', 'price', 'manufacturer', 'product_type',
                         'release_date', 'created_at', 'modified_at', 'attributes']
        # assertCountEquals checks for equal count of each item in the collection
        self.assertCountEqual(expected_keys, self.serializer.data.keys())


class WhenDeserializingAProductWithValidDataTests(TestCase):
    """This class defines the test suite for valid deserialization of a product."""

    @classmethod
    def setUpTestData(cls):
        cls.serializer_data = {
            "name": "Wrench",
            "price": 2.00,
            "manufacturer": "Allen",
            "product_type": "tool"
        }
        cls.serializer = ProductSerializer(data=cls.serializer_data)

    def test_serializer_should_find_data_to_be_valid(self):
        self.assertTrue(self.serializer.is_valid())


class WhenDeserializingAProductWithInvalidDataTests(TestCase):
    """This class defines the test suite for invalid deserialization of a product."""

    @classmethod
    def setUpTestData(cls):
        cls.serializer_data = {
            "name": "Wrench",
            "price": 2.00,
        }
        cls.serializer = ProductSerializer(data=cls.serializer_data)

    def test_serializer_should_find_data_to_be_valid(self):
        self.assertFalse(self.serializer.is_valid())
