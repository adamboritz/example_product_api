from django.conf.urls import url
from .views import AttributeList

urlpatterns = [
    url(r'^attributes/$', AttributeList.as_view(), name="attributes"),
]