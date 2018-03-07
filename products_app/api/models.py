from django.db import models
from django.utils import timezone


class Attribute(models.Model):
    """
    The representation of attribute. In a more complex system there would be a separate model for attribute types and
    those would be assigned to a product type and the attribute values would be related to the attribute type, but to
    limit the scope of this exercise, I've drastically oversimplified that representation.
    """
    type = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the representation of the attribute, showing the type and value"""
        return f"{self.type}: {self.value}"


class Product(models.Model):
    """
    The representation of a product with some fields that are consistent across all products, so to me they fit better
    here rather than as an attribute.
    """
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    manufacturer = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    release_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    attributes = models.ManyToManyField(Attribute)

    def __str__(self):
        """Return the representation of a product, it's name"""
        return f"{self.name}"
