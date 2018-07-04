from django.urls import path
from .views import SubscriberCreateView
from .views import CallRecordCreateListView
from .views import PriceCreateView

urlpatterns = [
    path(
        'subscriber/',
        SubscriberCreateView.as_view(),
        name="subscriber-create"
    ),
    path(
        'call_record/',
        CallRecordCreateListView.as_view(),
        name="call-record"
    ),
    path(
        'price/',
        PriceCreateView.as_view(),
        name="price-create"
    ),
]
