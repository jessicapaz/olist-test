from rest_framework.serializers import ModelSerializer

from .models import Subscriber
from .models import CallStartRecord
from .models import CallEndRecord
from .models import Price
from .models import BillRecord


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


class BillRecordSerializer(ModelSerializer):
    class Meta:
        model = BillRecord
        fields = ("call_duration","call_price")

    def to_representation(self, instance):
        data = super(BillRecordSerializer, self).to_representation(instance)
        data['destination'] = instance.call_start_record.destination
        data['call_start_date'] = instance.call_start_record.timestamp.date()
        data['call_start_time'] = instance.call_start_record.timestamp.time()
        return data
