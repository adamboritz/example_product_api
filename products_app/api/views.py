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
    """Displays multiple attributes, allows for filtering on the attributes collection and creation of new attributes"""
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('type', 'value')


class AttributeDetail(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          generics.GenericAPIView):
    """Displays an individual attribute and allows updating of the attribute"""
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class AttributeDelete(mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    """Handles deletion of an attribute"""
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

    def post(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProductList(generics.ListCreateAPIView):
    """Displays multiple products, allows for filtering on the products collection and creation of new products"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'price', 'manufacturer', 'product_type', 'release_date', 'created_at', 'modified_at',
                     'attributes__type', 'attributes__value')


class ProductDetail(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          generics.GenericAPIView):
    """Displays an individual product and allows updating of the product"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ProductDelete(mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    """Handles deletion of a product"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProductAddAttribute(mixins.UpdateModelMixin,
                          generics.GenericAPIView):
    """Allows for adding an attribute to a product"""
    queryset = Product.objects.all()
    serializer_class = ProductAddAttributeSerializer

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ProductRemoveAttribute(mixins.UpdateModelMixin,
                          generics.GenericAPIView):
    """Allows for adding an attribute to a product"""
    queryset = Product.objects.all()
    serializer_class = ProductRemoveAttributeSerializer

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
