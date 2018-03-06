import time
from datetime import datetime, timezone

from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


from .models import Attribute, Product
from .serializers import AttributeSerializer, ProductSerializer


class WhenAddingNewAttributeTests(TestCase):
    """This class defines the test suite for adding an attribute"""
    @classmethod
    def setUpClass(cls):
        cls.attribute_type = "Color"
        cls.attribute_value = "Red"
        cls.attribute = Attribute(type=cls.attribute_type, value=cls.attribute_value)
        cls.before_save_attribute_count = Attribute.objects.count()
        cls.attribute.save()

    @classmethod
    def tearDownClass(cls):
        Attribute.objects.all().delete()

    def test_attribute_count_should_be_one_higher_after_add(self):
        current_attribute_count = Attribute.objects.count()
        self.assertEqual(self.before_save_attribute_count + 1, current_attribute_count)

    def test_created_at_should_be_auto_populated(self):
        self.assertIsNotNone(self.attribute.created_at)

    def test_updated_at_should_be_auto_populated(self):
        self.assertIsNotNone(self.attribute.modified_at)


class WhenUpdatingAnAttributeTests(TestCase):
    """This class defines the test suite for updating an attribute"""

    @classmethod
    def setUpClass(cls):
        cls.attribute = Attribute(type="Color", value="Red")
        cls.attribute.save()
        cls.before_update_attribute_count = Attribute.objects.count()
        cls.before_update_created_at = cls.attribute.created_at
        cls.before_update_modified_at = cls.attribute.modified_at
        cls.attribute.value = "Blue"
        # Sometimes the test runs too quickly, so the sleep is inserted to ensure that the modified time is actually
        # different
        time.sleep(1)
        cls.attribute.save()

    @classmethod
    def tearDownClass(cls):
        Attribute.objects.all().delete()

    def test_attribute_count_should_not_change(self):
        current_attribute_count = Attribute.objects.count()
        self.assertEqual(self.before_update_attribute_count, current_attribute_count)

    def test_attribute_created_at_should_be_the_same(self):
        current_created_at = self.attribute.created_at
        self.assertEqual(current_created_at, self.before_update_created_at)

    def test_attribute_modified_at_should_be_updated(self):
        current_modified_at = self.attribute.modified_at
        self.assertNotEqual(current_modified_at, self.before_update_modified_at)

    def test_attribute_value_should_be_blue(self):
        self.assertEqual(self.attribute.value, "Blue")


class WhenDeletingAnAttributeTests(TestCase):
    """This class defines the test suite for deleting an attribute"""

    @classmethod
    def setUpClass(cls):
        cls.attribute1 = Attribute(type="Color", value="Red")
        cls.attribute1.save()
        cls.attribute2 = Attribute(type="Number Of Wheels", value="4")
        cls.attribute2.save()
        cls.attribute3 = Attribute(type="Backup camera", value="false")
        cls.attribute3.save()
        cls.before_delete_attribute_count = Attribute.objects.count()
        cls.attribute2.delete()

    @classmethod
    def tearDownClass(cls):
        Attribute.objects.all().delete()

    def test_attribute_count_should_decrease_by_one(self):
        current_attribute_count = Attribute.objects.count()
        self.assertEqual(self.before_delete_attribute_count - 1, current_attribute_count)

    def test_deleted_attribute_should_not_have_an_id(self):
        self.assertIsNone(self.attribute2.id)


class WhenAddingNewProductTests(TestCase):
    """This class defines the test suite for adding a product without providing a release date"""
    @classmethod
    def setUpClass(cls):
        cls.product = Product(name="Apple iPhoneX", price=999.99, manufacturer="Apple", product_type="Smartphone")
        cls.before_save_product_count = Product.objects.count()
        cls.product.save()

    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()

    def test_product_count_should_be_one_higher_after_add(self):
        current_product_count = Product.objects.count()
        self.assertEqual(self.before_save_product_count + 1, current_product_count)

    def test_created_at_should_be_auto_populated(self):
        self.assertIsNotNone(self.product.created_at)

    def test_updated_at_should_be_auto_populated(self):
        self.assertIsNotNone(self.product.modified_at)

    def test_release_date_should_be_auto_populated(self):
        self.assertIsNotNone(self.product.release_date)


class WhenAddingNewProductWithReleaseDateTests(TestCase):
    """This class defines the test suite for adding a product with a release date"""
    @classmethod
    def setUpClass(cls):
        cls.passedInDateTime = datetime(2017, 6, 1, tzinfo=timezone.utc)
        cls.product = Product(name="Apple iPhoneX", price=999.99, manufacturer="Apple", product_type="Smartphone",
                              release_date=cls.passedInDateTime)
        cls.before_save_product_count = Product.objects.count()
        cls.product.save()

    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()

    def test_release_date_should_be_provided_value(self):
        self.assertEqual(self.product.release_date, self.passedInDateTime)


class WhenUpdatingAProductTests(TestCase):
    """This class defines the test suite for updating a product"""

    @classmethod
    def setUpClass(cls):
        cls.product = Product(name="Apple iPhoneX", price=999.99, manufacturer="Apple", product_type="Smartphone")
        cls.product.save()
        cls.before_update_product_count = Product.objects.count()
        cls.before_update_created_at = cls.product.created_at
        cls.before_update_modified_at = cls.product.modified_at
        cls.product.manufacturer = "Apple, Inc."

        # Sometimes the test runs too quickly, so the sleep is inserted to ensure that the modified time is actually
        # different
        time.sleep(1)
        cls.product.save()

    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()

    def test_product_count_should_not_change(self):
        current_product_count = Product.objects.count()
        self.assertEqual(self.before_update_product_count, current_product_count)

    def test_product_created_at_should_be_the_same(self):
        current_created_at = self.product.created_at
        self.assertEqual(current_created_at, self.before_update_created_at)

    def test_product_modified_at_should_be_updated(self):
        current_modified_at = self.product.modified_at
        self.assertNotEqual(current_modified_at, self.before_update_modified_at)

    def test_product_manufacturer_should_be_updated(self):
        self.assertEqual(self.product.manufacturer, "Apple, Inc.")


class WhenUpdatingAProductReleaseDateTests(TestCase):
    """This class defines the test suite for updating a product's release date"""

    @classmethod
    def setUpClass(cls):
        cls.product = Product(name="Apple iPhoneX", price=999.99, manufacturer="Apple", product_type="Smartphone")
        cls.product.save()
        cls.before_update_release_date = cls.product.release_date
        cls.product.release_date = datetime(2017, 6, 1, tzinfo=timezone.utc)
        cls.product.save()

    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()

    def test_product_release_date_should_update(self):
        self.assertEqual(self.product.release_date, datetime(2017, 6, 1, tzinfo=timezone.utc))


class WhenDeletingProductWithoutAttributesTests(TestCase):
    """This class defines the test suite for deleting a product"""

    @classmethod
    def setUpClass(cls):
        cls.product1 = Product(name="iWatch", price=399.99)
        cls.product1.save()
        cls.product2 = Product(name="Logitech MX Mouse", price=99.99)
        cls.product2.save()
        cls.product3 = Product(name="HP Laptop", price=1299.99)
        cls.product3.save()
        cls.before_delete_product_count = Product.objects.count()
        cls.product2.delete()

    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()

    def test_product_count_should_decrease_by_one(self):
        current_product_count = Product.objects.count()
        self.assertEqual(self.before_delete_product_count - 1, current_product_count)

    def test_deleted_product_should_not_have_an_id(self):
        self.assertIsNone(self.product2.id)

class WhenAddingMultipleAttributesToAProductTests(TestCase):
    """This class defines the test suite for adding multiple attributes to a product"""

    @classmethod
    def setUpClass(cls):
        cls.product1 = Product(name="Tesla Model 3", price=40000.00)
        cls.product1.save()
        cls.attribute1 = Attribute(type="Color", value="Red")
        cls.attribute1.save()
        cls.attribute2 = Attribute(type="Number Of Wheels", value="4")
        cls.attribute2.save()
        cls.product1.attributes.add(cls.attribute1, cls.attribute2)

    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()
        Attribute.objects.all().delete()

    def test_product_should_have_two_attributes(self):
        self.assertEqual(self.product1.attributes.all().count(), 2)


class WhenAddingAnAttributeToMultipleProductTests(TestCase):
    """This class defines the test suite for adding an attribute to multiple product"""

    @classmethod
    def setUpClass(cls):
        cls.product1 = Product(name="Tesla Model 3", price=40000.00)
        cls.product1.save()
        cls.product2 = Product(name="Honda Accord", price=20000.00)
        cls.product2.save()
        cls.attribute1 = Attribute(type="Number Of Wheels", value="4")
        cls.attribute1.save()
        cls.product1.attributes.add(cls.attribute1)
        cls.product2.attributes.add(cls.attribute1)

    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()
        Attribute.objects.all().delete()

    def test_attribute_should_be_associated_to_two_products(self):
        self.assertEqual(self.attribute1.product_set.all().count(), 2)


class WhenDeletingAProductWithAttributesTests(TestCase):
    """This class defines the test suite for deleting a product with multiple attributes assigned to it"""

    @classmethod
    def setUpClass(cls):
        cls.product1 = Product(name="Tesla Model 3", price=40000.00)
        cls.product1.save()
        cls.attribute1 = Attribute(type="Color", value="Red")
        cls.attribute1.save()
        cls.attribute2 = Attribute(type="Number Of Wheels", value="4")
        cls.attribute2.save()
        cls.product1.attributes.add(cls.attribute1, cls.attribute2)
        cls.product1.delete()

    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()
        Attribute.objects.all().delete()

    def test_attributes_should_not_be_deleted(self):
        self.assertIsNotNone(self.attribute1.id)
        self.assertIsNotNone(self.attribute2.id)


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


class WhenSendingAGetToAttributesView(TestCase):
    """This class defines the test suite for a GET request to the attributes view"""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.response = cls.client.get(
            reverse("attributes"),
            format="json"
        )

    def test_should_receive_a_200_ok_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_200_OK)


class WhenSendingAPostToAttributesView(TestCase):
    """This class defines the test suite for a POST request to the attributes view"""

    @classmethod
    def setUpTestData(cls):
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

    @classmethod
    def tearDownClass(cls):
        Attribute.objects.all().delete()

    def test_should_receive_a_201_created_response(self):
        self.assertTrue(self.response.status_code, status.HTTP_201_CREATED)

    def test_should_have_an_id_for_created_attribute(self):
        self.assertIn(b"id", self.response.content)
