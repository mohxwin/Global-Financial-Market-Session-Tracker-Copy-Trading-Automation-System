from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from referrals.models import Referral, ReferralCode
from referrals.serializers import ReferralSerializer, ReferralCodeSerializer

# Create your views here.

class ReferralCodeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        referral_codes = ReferralCode.objects.filter(referrer=request.user)
        serializer = ReferralCodeSerializer(referral_codes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReferralView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        referrals = Referral.objects.filter(referrer=request.user)
        serializer = ReferralSerializer(referrals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ReferralSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(referrer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)