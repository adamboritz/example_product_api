from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import mixins

from .models import Attribute
from .models import Product
from .serializers import AttributeSerializer
from .serializers import ProductAddAttributeSerializer
from .serializers import ProductRemoveAttributeSerializer
from .serializers import ProductSerializer


class AttributeList(generics.ListCreateAPIView):
    """
    get:
    Return a list of all the existing attributes. Can be filtered down on type or value.

    post:
    Creates a new attribute.
    """
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('type', 'value')


class AttributeDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    get:
    Return an individual attribute.

    post:
    Updates an individual attribute.
    """
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class AttributeDelete(mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    post:
    Deletes an individual attribute.
    """
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

    def post(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProductList(generics.ListCreateAPIView):
    """
    get:
    Return a list of all the existing products. Can be filtered down on all product non-id fields and attribute type and
    attribute value.

    post:
    Creates a new product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'price', 'manufacturer', 'product_type', 'release_date', 'created_at', 'modified_at',
                     'attributes__type', 'attributes__value')


class ProductDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    get:
    Return an individual product.

    post:
    Updates an individual product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ProductDelete(mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    post:
    Deletes an individual product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProductAddAttribute(mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    post:
    Adds specified attribute to specified product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductAddAttributeSerializer

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ProductRemoveAttribute(mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    post:
    Removes specified attribute from specified product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductRemoveAttributeSerializer

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
