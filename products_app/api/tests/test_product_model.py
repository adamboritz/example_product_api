import time
from datetime import datetime
from datetime import timezone

from .test_case_with_fixture_data import TestCaseWithFixtureData
from api.models import Product


class WhenAddingNewProductTests(TestCaseWithFixtureData):
    """This class defines the test suite for adding a product without providing a release date"""
    @classmethod
    def setUpClass(cls):
        super(WhenAddingNewProductTests, cls).setUpTestData()

        cls.product = Product(name="Apple iPhoneX", price=999.99, manufacturer="Apple", product_type="Smartphone")
        cls.before_save_product_count = Product.objects.count()
        cls.product.save()

    def test_product_count_should_be_one_higher_after_add(self):
        current_product_count = Product.objects.count()
        self.assertEqual(self.before_save_product_count + 1, current_product_count)

    def test_created_at_should_be_auto_populated(self):
        self.assertIsNotNone(self.product.created_at)

    def test_updated_at_should_be_auto_populated(self):
        self.assertIsNotNone(self.product.modified_at)

    def test_release_date_should_be_auto_populated(self):
        self.assertIsNotNone(self.product.release_date)


class WhenAddingNewProductWithReleaseDateTests(TestCaseWithFixtureData):
    """This class defines the test suite for adding a product with a release date"""
    @classmethod
    def setUpClass(cls):
        super(WhenAddingNewProductWithReleaseDateTests, cls).setUpTestData()

        cls.passedInDateTime = datetime(2017, 6, 1, tzinfo=timezone.utc)
        cls.product = Product(name="Apple iPhoneX", price=999.99, manufacturer="Apple", product_type="Smartphone",
                              release_date=cls.passedInDateTime)
        cls.product.save()

    def test_release_date_should_be_provided_value(self):
        self.assertEqual(self.product.release_date, self.passedInDateTime)


class WhenUpdatingAProductTests(TestCaseWithFixtureData):
    """This class defines the test suite for updating a product"""

    @classmethod
    def setUpClass(cls):
        super(WhenUpdatingAProductTests, cls).setUpTestData()

        cls.before_update_product_count = Product.objects.count()
        cls.before_update_created_at = cls.product1.created_at
        cls.before_update_modified_at = cls.product1.modified_at
        cls.product1.manufacturer = "Apple, Inc."

        # Sometimes the test runs too quickly, so the sleep is inserted to ensure that the modified time is actually
        # different
        time.sleep(1)
        cls.product1.save()

    def test_product_count_should_not_change(self):
        current_product_count = Product.objects.count()
        self.assertEqual(self.before_update_product_count, current_product_count)

    def test_product_created_at_should_be_the_same(self):
        current_created_at = self.product1.created_at
        self.assertEqual(current_created_at, self.before_update_created_at)

    def test_product_modified_at_should_be_updated(self):
        current_modified_at = self.product1.modified_at
        self.assertNotEqual(current_modified_at, self.before_update_modified_at)

    def test_product_manufacturer_should_be_updated(self):
        self.assertEqual(self.product1.manufacturer, "Apple, Inc.")


class WhenUpdatingAProductReleaseDateTests(TestCaseWithFixtureData):
    """This class defines the test suite for updating a product's release date"""

    @classmethod
    def setUpClass(cls):
        super(WhenUpdatingAProductReleaseDateTests, cls).setUpTestData()

        cls.before_update_release_date = cls.product1.release_date
        cls.product1.release_date = datetime(2017, 6, 1, tzinfo=timezone.utc)
        cls.product1.save()

    def test_product_release_date_should_update(self):
        self.assertEqual(self.product1.release_date, datetime(2017, 6, 1, tzinfo=timezone.utc))


class WhenDeletingProductWithoutAttributesTests(TestCaseWithFixtureData):
    """This class defines the test suite for deleting a product"""

    @classmethod
    def setUpClass(cls):
        super(WhenDeletingProductWithoutAttributesTests, cls).setUpTestData()

        cls.before_delete_product_count = Product.objects.count()
        cls.product2.delete()

    def test_product_count_should_decrease_by_one(self):
        current_product_count = Product.objects.count()
        self.assertEqual(self.before_delete_product_count - 1, current_product_count)

    def test_deleted_product_should_not_have_an_id(self):
        self.assertIsNone(self.product2.id)


class WhenAddingMultipleAttributesToAProductTests(TestCaseWithFixtureData):
    """This class defines the test suite for adding multiple attributes to a product"""

    @classmethod
    def setUpClass(cls):
        super(WhenAddingMultipleAttributesToAProductTests, cls).setUpTestData()

        cls.product1.attributes.add(cls.attribute1, cls.attribute2)

    def test_product_should_have_two_attributes(self):
        self.assertEqual(self.product1.attributes.all().count(), 2)


class WhenAddingAnAttributeToMultipleProductTests(TestCaseWithFixtureData):
    """This class defines the test suite for adding an attribute to multiple product"""

    @classmethod
    def setUpClass(cls):
        super(WhenAddingAnAttributeToMultipleProductTests, cls).setUpTestData()

        cls.product1.attributes.add(cls.attribute1)
        cls.product2.attributes.add(cls.attribute1)

    def test_attribute_should_be_associated_to_two_products(self):
        self.assertEqual(self.attribute1.product_set.all().count(), 2)


class WhenDeletingAProductWithAttributesTests(TestCaseWithFixtureData):
    """This class defines the test suite for deleting a product with multiple attributes assigned to it"""

    @classmethod
    def setUpClass(cls):
        super(WhenDeletingAProductWithAttributesTests, cls).setUpTestData()

        cls.product1.attributes.add(cls.attribute1, cls.attribute2)
        cls.product1.delete()

    def test_attributes_should_not_be_deleted(self):
        self.assertIsNotNone(self.attribute1.id)
        self.assertIsNotNone(self.attribute2.id)
