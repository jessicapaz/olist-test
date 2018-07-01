from django.urls import path
from .views import SubscriberCreateView


urlpatterns = [
    path(
        'subscriber/', 
        SubscriberCreateView.as_view(), 
        name="subscriber-create"
    )
]