from rest_framework import serializers
from referrals.models import Referral, ReferralCode

class ReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = ['id', 'code', 'created_at']
    
    
class ReferralSerializer(serializers.ModelSerializer):
    referred_user_username = serializers.CharField(source='referred_user.username', read_only=True)
    class Meta:
        model = Referral
        fields = ['id', 'referrer', 'referred_user', 'referred_user_username', 'created_at']
        