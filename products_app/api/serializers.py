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
        fields = ('id', 'name', 'price', 'manufacturer', 'product_type',
                  'release_date', 'created_at', 'modified_at', 'attributes')
        read_only_fields = ('id', 'created_at', 'modified_at')


class ProductAddAttributeSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(read_only=True, many=True)
    attribute_id = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), write_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'manufacturer', 'product_type',
                  'release_date', 'created_at', 'modified_at', 'attributes', 'attribute_id')
        read_only_fields = ('id', 'name', 'price', 'manufacturer', 'product_type',
                            'release_date', 'created_at', 'modified_at')

    def update(self, instance, validated_data):
        product = Product.objects.get(pk=instance.id)
        attribute_id = validated_data.pop("attribute_id")
        product.attributes.add(attribute_id)
        return product


class ProductRemoveAttributeSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(read_only=True, many=True)
    attribute_id = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all(), write_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'manufacturer', 'product_type',
                  'release_date', 'created_at', 'modified_at', 'attributes', 'attribute_id')
        read_only_fields = ('id', 'name', 'price', 'manufacturer', 'product_type',
                            'release_date', 'created_at', 'modified_at')

    def update(self, instance, validated_data):
        product = Product.objects.get(pk=instance.id)
        attribute_id = validated_data.pop("attribute_id")
        product.attributes.remove(attribute_id)
        return product
