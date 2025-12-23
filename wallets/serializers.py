from rest_framework import serializers
from .models import CoinWallet

class CoinWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinWallet
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')