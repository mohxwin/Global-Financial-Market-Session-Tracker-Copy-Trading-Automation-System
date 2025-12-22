from rest_framework import serializers
from .models import CostumeUser



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CostumeUser
        fields = ["first_name", "last_name", "email", "password", "role"]

    def create(self, validated_data):
        user = CostumeUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user


class TwoFAVerifySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    otp = serializers.CharField(max_length=6)
