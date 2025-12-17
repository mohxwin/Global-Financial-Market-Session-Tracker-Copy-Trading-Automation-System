from rest_framework import serializers
from .models import User



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "full_name", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user


class TwoFAVerifySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    otp = serializers.CharField(max_length=6)
