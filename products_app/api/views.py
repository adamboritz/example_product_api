from rest_framework import generics
from rest_framework import mixins

from .models import Attribute
from .models import Product
from .serializers import AttributeSerializer
from .serializers import ProductSerializer


class AttributeList(generics.ListCreateAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class AttributeDetail(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          generics.GenericAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class AttributeDelete(mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

    def post(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ProductDelete(mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
