import time

from django.test import TestCase

from api.models import Attribute


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
