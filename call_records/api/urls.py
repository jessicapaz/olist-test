from django.urls import path, re_path
from .views import SubscriberCreateView
from .views import CallRecordCreateListView
from .views import PriceCreateView
from .views import BillRecordView

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
    path(
        'bill_record/<slug:phone_number>/',
        BillRecordView.as_view(),
        name="bill-record"
    ),
]
