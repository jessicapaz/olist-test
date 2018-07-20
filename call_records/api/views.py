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
from rest_framework.viewsets import ViewSet


class SubscriberViewSet(ViewSet):
    """
    **POST**
    Create a new subscriber instance.

    **GET (Retrieve)**:
    Return the given subscriber.

    **GET (List)**:
    Return a list of all subscribers.

    **DELETE**:
    Delete the given subscriber.
    """
    queryset = Subscriber.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)

    def create(self, request, *args, **kwargs):
        serializer = SubscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        serializer = SubscriberSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        subscriber = get_object_or_404(self.queryset, pk=pk)
        serializer = SubscriberSerializer(subscriber)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        subscriber = get_object_or_404(Subscriber, pk=pk)
        subscriber.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        call_type = request.data.get('type', None)
        request_data = self.get_request_data(call_type, request)
        try:
            get_serializer = self.get_call_serializer(call_type)
        except TypeError:
            error_message = 'detail: type must be start or end.'
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        serializer = get_serializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_request_data(self, call_type, request):
        if call_type:
            request_data = request.data.copy()
            request_data.pop('type')
            return request_data
        else:
            error_message = 'detail: type is required.'
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    def get_call_serializer(self, call_type):
        if call_type == 'start':
            return CallStartRecordSerializer
        elif call_type == 'end':
            return CallEndRecordSerializer
        else:
            raise TypeError


class PriceViewSet(ViewSet):
    """
    **POST**
    Create a new price instance.

    **GET (Retrieve)**:
    Return the given price.

    **GET (List)**:
    Return a list of all prices.

    **DELETE**:
    Delete the given price.
    """
    queryset = Price.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)

    def create(self, request, *args, **kwargs):
        serializer = PriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        serializer = PriceSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        price = get_object_or_404(Price, pk=pk)
        serializer = PriceSerializer(price)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        price = get_object_or_404(Price, pk=pk)
        price.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BillRecordView(APIView):
    """
    Return a bill records list of one subscriber.
    """
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, *args, **kwargs):
        month, year = self.get_previous_month()
        month = request.GET.get('month', month)
        year = request.GET.get('year', year)
        phone_number = kwargs.get('phone_number')
        subscriber = get_object_or_404(Subscriber, phone_number=phone_number)
        bills = self.get_bill_queryset(subscriber, month, year)
        data = self.get_bill_data(subscriber, bills)
        return Response(data, status.HTTP_200_OK)

    def get_bill_queryset(self, subscriber, month, year):
        bills = BillRecord.objects.filter(
            subscriber=subscriber,
            reference_month=month,
            reference_year=year
        )
        return bills

    def get_bill_data(self, subscriber, bills):
        subscriber_name = f'{subscriber.first_name} {subscriber.last_name}'
        total_price = bills.aggregate(Sum('call_price'))
        data = {
            'subscriber': subscriber_name,
            'total_price': total_price['call_price__sum'],
            'bill_records': BillRecordSerializer(bills, many=True).data
        }
        return data

    def get_previous_month(self):
        current_month = timezone.now().month
        if current_month == 1:
            month = current_month + 11
            year = timezone.now().year - 1
        else:
            month = current_month - 1
            year = timezone.now().year
        return month, year
