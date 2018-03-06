from django.conf.urls import url

from .views import AttributeList
from .views import ProductList

urlpatterns = [
    url(r'^attributes/$', AttributeList.as_view(), name="attributes"),
    url(r'^attributes/(?P<pk>[0-9]+)/$', AttributeList.as_view(), name="attribute_details"),
    url(r'^products/$', ProductList.as_view(), name="products"),
]