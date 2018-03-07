from django.conf.urls import url

from .views import AttributeDetail
from .views import AttributeDelete
from .views import AttributeList
from .views import ProductAddAttribute
from .views import ProductRemoveAttribute
from .views import ProductDetail
from .views import ProductDelete
from .views import ProductList

urlpatterns = [
    url(r'^attributes/$', AttributeList.as_view(), name="attributes"),
    url(r'^attributes/(?P<pk>[0-9]+)/$', AttributeDetail.as_view(), name="attribute_details"),
    url(r'^attributes/(?P<pk>[0-9]+)/delete/$', AttributeDelete.as_view(), name="attribute_delete"),
    url(r'^products/$', ProductList.as_view(), name="products"),
    url(r'^products/(?P<pk>[0-9]+)/$', ProductDetail.as_view(), name="product_details"),
    url(r'^products/(?P<pk>[0-9]+)/delete/$', ProductDelete.as_view(), name="product_delete"),
    url(r'^products/(?P<pk>[0-9]+)/add-attribute/$', ProductAddAttribute.as_view(), name="product_add_attribute"),
    url(r'^products/(?P<pk>[0-9]+)/remove-attribute/$', ProductRemoveAttribute.as_view(),
        name="product_remove_attribute")
]
