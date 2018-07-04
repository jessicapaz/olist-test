from rest_framework.serializers import ModelSerializer

from .models import Subscriber
from .models import CallStartRecord
from .models import CallEndRecord
from .models import Price


class SubscriberSerializer(ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'


class CallStartRecordSerializer(ModelSerializer):
    class Meta:
        model = CallStartRecord
        fields = '__all__'


class CallEndRecordSerializer(ModelSerializer):
    class Meta:
        model = CallEndRecord
        fields = '__all__'


class PriceSerializer(ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
