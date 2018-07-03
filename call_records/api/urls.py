from django.urls import path
from .views import SubscriberCreateView
from .views import CallRecordCreateListView

urlpatterns = [
    path(
        'subscriber/',
        SubscriberCreateView.as_view(),
        name="subscriber-create"
    ),
    path(
        'call_record/',
        CallRecordCreateListView.as_view()
    ),
]
