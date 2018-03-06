from rest_framework import generics

from .models import Attribute
from .serializers import AttributeSerializer


class AttributeList(generics.ListCreateAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
