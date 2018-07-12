from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Sum

from .models import Subscriber
from .models import CallStartRecord
from .models import CallEndRecord
from .models import Price
from .models import BillRecord

from .serializers import CallStartRecordSerializer
from .serializers import CallEndRecordSerializer
from .serializers import SubscriberSerializer
from .serializers import PriceSerializer
from .serializers import BillRecordSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView


class SubscriberCreateView(CreateAPIView):
    """
    Create a new subscriber instance.
    """
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


class CallRecordCreateListView(APIView):
    """
    **GET:**
    Return a list of all call records.

    **POST:**
    Create a new call record instance.
    """
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, format=None):
        call_start_records = CallStartRecord.objects.all()
        call_end_records = CallEndRecord.objects.all()
        call_start_serializer = CallStartRecordSerializer(
            call_start_records, many=True
        ).data
        call_end_serializer = CallEndRecordSerializer(
            call_end_records, many=True
        ).data
        data = {
            'call_start_records': call_start_serializer,
            'call_end_records': call_end_serializer
        }
        return Response(data, status.HTTP_200_OK)

    def post(self, request, format=None):
        call_type = request.data.get('type')
        request_data = request.data.copy()
        request_data.pop('type')
        if call_type == 'start':
            serializer = CallStartRecordSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif call_type == 'end':
            serializer = CallEndRecordSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PriceCreateView(CreateAPIView):
    """
    Create a new price instance.
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)


class BillRecordView(APIView):
    """
    Return a bill records list of one subscriber.
    """
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, *args, **kwargs):
        current_month = timezone.now().month
        if current_month == 1:
            month =  current_month + 11
            year = timezone.now().year - 1
        else:
            month =  current_month - 1
            year =  timezone.now().year
        month = request.GET.get('month', month)
        year = request.GET.get('year', year)
        phone_number = kwargs.get('phone_number')
        subscriber = get_object_or_404(Subscriber, phone_number=phone_number)
        bills = BillRecord.objects.filter(
            subscriber=subscriber, 
            reference_month=month,
            reference_year=year
        )
        subscriber_name = f'{subscriber.first_name} {subscriber.last_name}'
        total_price = bills.aggregate(Sum('call_price'))
        data = {
            'subscriber': subscriber_name,
            'total_price': total_price['call_price__sum'],
            'bill_records': BillRecordSerializer(bills, many=True).data
        } 
        return Response(data, status.HTTP_200_OK)
