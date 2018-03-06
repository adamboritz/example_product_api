from django.test import TestCase

from api.models import Attribute
from api.serializers import AttributeSerializer


class WhenSerializingAnAttributeTests(TestCase):
    """This class defines the test suite for serializing an attribute."""

    @classmethod
    def setUpTestData(cls):
        cls.attribute = Attribute(type="Color", value="Red")
        cls.attribute.save()
        cls.serializer = AttributeSerializer(instance=cls.attribute)

    @classmethod
    def tearDownClass(cls):
        Attribute.objects.all().delete()

    # As there is no custom behavior being specified, just need to test to ensure the one thing that we control is
    # being tested
    def test_keys_should_match_supplied_list(self):
        expected_keys = ['id', 'type', 'value', 'created_at', 'modified_at']
        # assertCountEquals checks for equal count of each item in the collection
        self.assertCountEqual(expected_keys, self.serializer.data.keys())


class WhenDeserializingAnAttributeWithValidDataTests(TestCase):
    """This class defines the test suite for valid deserialization of an attribute."""

    @classmethod
    def setUpTestData(cls):
        cls.serializer_data = {
            "type": "Media Format",
            "value": "CD",
        }
        cls.serializer = AttributeSerializer(data=cls.serializer_data)

    def test_serializer_should_find_data_to_be_valid(self):
        self.assertTrue(self.serializer.is_valid())


class WhenDeserializingAnAttributeWithInvalidDataTests(TestCase):
    """This class defines the test suite for invalid deserialization of an attribute."""

    @classmethod
    def setUpTestData(cls):
        cls.serializer_data = {
            "type": {"something": "Media Format"},
            "value": [1, 2, 3],
        }
        cls.serializer = AttributeSerializer(data=cls.serializer_data)

    def test_serializer_should_find_data_to_be_valid(self):
        self.assertFalse(self.serializer.is_valid())

    def serializer_errors_should_contain_invalid_field(self):
        # assertCountEquals checks for equal count of each item in the collection
        self.assertCountEqual(self.serializer.errors, ['type', 'value'])
