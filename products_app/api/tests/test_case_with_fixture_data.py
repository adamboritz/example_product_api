from django.test import TestCase

from api.models import Attribute
from api.models import Product


class TestCaseWithFixtureData(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product1 = Product(name="iWatch", price=399.99, manufacturer="Apple", product_type="Smartwatch")
        cls.product1.save()
        cls.product2 = Product(name="Logitech MX Mouse", price=99.99, manufacturer="Logitech", product_type="Mouse")
        cls.product2.save()
        cls.product3 = Product(name="HP Laptop", price=1299.99, manufacturer="HP", product_type="Laptop")
        cls.product3.save()

        cls.attribute1 = Attribute(type="Color", value="Red")
        cls.attribute1.save()
        cls.attribute2 = Attribute(type="Number Of Wheels", value="4")
        cls.attribute2.save()
        cls.attribute3 = Attribute(type="Backup camera", value="false")
        cls.attribute3.save()
        pass

    @classmethod
    def tearDownClass(cls):
        Product.objects.all().delete()
        Attribute.objects.all().delete()
