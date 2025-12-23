from rest_framework import serializers
from .models import TradeProfile, ExchangeAccount, Trade, TradeSession

class TradeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')


class ExchangeAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeAccount
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    
class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'
        read_only_fields = ('symbol','created_at', 'updated_at')

class TradeSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeSession
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')