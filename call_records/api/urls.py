from django.urls import path, include

from rest_framework_jwt.views import obtain_jwt_token

from .views import SubscriberViewSet
from .views import CallRecordCreateListView
from .views import PriceViewSet
from .views import BillRecordView

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('subscriber', SubscriberViewSet, base_name='subscriber')
router.register('price', PriceViewSet, base_name='price')

urlpatterns = [
    path(
        'auth/',
        obtain_jwt_token
    ),
    path(
        'call-record/',
        CallRecordCreateListView.as_view(),
        name="call-record"
    ),
    path(
        'bill-record/<slug:phone_number>/',
        BillRecordView.as_view(),
        name="bill-record"
    ),
]
urlpatterns += router.urls