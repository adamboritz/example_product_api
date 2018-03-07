from .test_case_with_fixture_data import TestCaseWithFixtureData
from api.serializers import ProductSerializer


class WhenSerializingAProductTests(TestCaseWithFixtureData):
    """This class defines the test suite for serializing a product."""

    @classmethod
    def setUpTestData(cls):
        super(WhenSerializingAProductTests, cls).setUpTestData()

        cls.serializer = ProductSerializer(instance=cls.product1)

    # As there is no custom behavior being specified, just need to test to ensure the one thing that we control is
    # being tested
    def test_keys_should_match_supplied_list(self):
        expected_keys = ['id', 'name', 'price', 'manufacturer', 'product_type',
                         'release_date', 'created_at', 'modified_at', 'attributes']
        # assertCountEquals checks for equal count of each item in the collection
        self.assertCountEqual(expected_keys, self.serializer.data.keys())


class WhenDeserializingAProductWithValidDataTests(TestCaseWithFixtureData):
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


class WhenDeserializingAProductWithInvalidDataTests(TestCaseWithFixtureData):
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
