from django.shortcuts import render

from .models import Subscriber
from .models import CallStartRecord
from .models import CallEndRecord
from .models import Price

from .serializers import CallStartRecordSerializer
from .serializers import CallEndRecordSerializer
from .serializers import SubscriberSerializer
from .serializers import PriceSerializer

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
    **get:**
    Return a list of all call records.

    **post:**
    Create a new call record instance.
    """
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, format=None):

        data = {
            'call_start_records': CallStartRecordSerializer(
                CallStartRecord.objects.all(), many=True
                ).data,
            'call_end_records': CallEndRecordSerializer(
                CallEndRecord.objects.all(), many=True
                ).data
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