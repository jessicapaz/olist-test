from django.shortcuts import render

from .models import Subscriber
from .models import CallStartRecord

from .serializers import CallStartRecordSerializer
from .serializers import CallEndRecordSerializer
from .serializers import SubscriberSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView


class SubscriberCreateView(CreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)



class CallRecordCreateView(APIView):
    # permission_classes = ()

    def post(self, request, format=None):
        if request.data.get('type') == 'end':
            request_data = request.data.copy()
            request_data.pop('type')
            serializer = CallEndRecordSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.data.get('type') == 'start':
            request_data = request.data.copy()
            request_data.pop('type')
            serializer = CallStartRecordSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
