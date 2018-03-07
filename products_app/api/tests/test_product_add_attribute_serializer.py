from .test_case_with_fixture_data import TestCaseWithFixtureData
from api.serializers import ProductAddAttributeSerializer


class WhenSerializingWithProductAddAttributeTests(TestCaseWithFixtureData):
    """This class defines the test suite for serializing a product and attribute id."""

    @classmethod
    def setUpTestData(cls):
        super(WhenSerializingWithProductAddAttributeTests, cls).setUpTestData()

        cls.serializer = ProductAddAttributeSerializer(instance=cls.product1)

    # As there is no custom behavior being specified, just need to test to ensure the one thing that we control is
    # being tested
    def test_keys_should_match_supplied_list(self):
        expected_keys = ['id', 'name', 'price', 'manufacturer', 'product_type',
                         'release_date', 'created_at', 'modified_at', 'attributes']
        # assertCountEquals checks for equal count of each item in the collection
        self.assertCountEqual(expected_keys, self.serializer.data.keys())


class WhenDeserializingAProductAddAttributeWithValidDataTests(TestCaseWithFixtureData):
    """This class defines the test suite for valid deserialization of a product and attribute id."""

    @classmethod
    def setUpTestData(cls):
        super(WhenDeserializingAProductAddAttributeWithValidDataTests, cls).setUpTestData()

        cls.serializer_data = {
            "attribute_id": str(cls.attribute1.id),
        }
        cls.serializer = ProductAddAttributeSerializer(data=cls.serializer_data)

    def test_serializer_should_find_data_to_be_valid(self):
        self.assertTrue(self.serializer.is_valid())


class WhenDeserializingAProductAddAttributeWithInvalidDataTests(TestCaseWithFixtureData):
    """This class defines the test suite for valid deserialization of a product and attribute id."""

    @classmethod
    def setUpTestData(cls):
        super(WhenDeserializingAProductAddAttributeWithInvalidDataTests, cls).setUpTestData()

        cls.serializer_data = {
            "attribute_id": "akkb",
            "id": "2"
        }
        cls.serializer = ProductAddAttributeSerializer(data=cls.serializer_data)

    def test_serializer_should_find_data_to_be_invalid(self):
        self.assertFalse(self.serializer.is_valid())
