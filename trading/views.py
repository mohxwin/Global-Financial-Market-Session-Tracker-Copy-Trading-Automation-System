from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import TradeProfile, ExchangeAccount, Trade, TradeSession
from .serializers import (TradeProfileSerializer, ExchangeAccountSerializer, TradeSerializer, 
                          TradeSessionSerializer)


# Create your views here.

class TradeProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trade_profiles = TradeProfile.objects.filter(user=request.user)
        serializer = TradeProfileSerializer(trade_profiles, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = TradeProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ExchangeAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        exchange_accounts = ExchangeAccount.objects.filter(user=request.user)
        serializer = ExchangeAccountSerializer(exchange_accounts, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = ExchangeAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    
class TradeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trades = Trade.objects.filter(trade_profile__user=request.user)
        serializer = TradeSerializer(trades, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = TradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TradeSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trade_sessions = TradeSession.objects.all()
        serializer = TradeSessionSerializer(trade_sessions, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = TradeSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)