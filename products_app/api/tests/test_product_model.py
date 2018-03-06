import time
from datetime import datetime
from datetime import timezone

from django.test import TestCase

from api.models import Attribute
from api.models import Product


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
