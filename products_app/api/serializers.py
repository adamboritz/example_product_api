from rest_framework import serializers

from .models import Attribute
from .models import Product


class AttributeSerializer(serializers.ModelSerializer):
    """Definition for how to serialize an Attribute"""
    class Meta:
        model = Attribute
        fields = ('id', 'type', 'value', 'created_at', 'modified_at')
        read_only_fields = ('id', 'created_at', 'modified_at')


class ProductSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(read_only=True, many=True)
    class Meta:
        model = Product
        fields = ('id','name', 'price', 'manufacturer', 'product_type',
                  'release_date', 'created_at', 'modified_at', 'attributes')
        read_only_fields = ('id', 'created_at', 'modified_at')
