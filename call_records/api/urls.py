from django.urls import path
from .views import SubscriberCreateView
from .views import CallRecordCreateView

urlpatterns = [
    path(
        'subscriber/', 
        SubscriberCreateView.as_view(), 
        name="subscriber-create"
    ),
    path(
        'call_record/',
        CallRecordCreateView.as_view()
    ),
]