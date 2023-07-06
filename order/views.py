from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config.tasks import send_notification_email_task
from . import serializers


class CreateOrderView(ListCreateAPIView):
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = request.user
        orders = user.orders.all()
        serializer = serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data, status=200)
