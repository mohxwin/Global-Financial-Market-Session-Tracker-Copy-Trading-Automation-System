from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CoinWallet
from .serializers import CoinWalletSerializer


# Create your views here.

class CoinWalletView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        wallets = CoinWallet.objects.filter(user=request.user)
        serializer = CoinWalletSerializer(wallets, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CoinWalletSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    