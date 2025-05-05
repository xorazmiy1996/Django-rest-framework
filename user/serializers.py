from .models import UserBalance
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from django.core.validators import MinValueValidator


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=30)
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Parolni hash qiladi
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])  # Parolni yangilaydi

        instance.save()
        return instance


class UserDetailSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'balance']

    def get_balance(self, obj):
        balance = UserBalance.objects.get(user=obj)
        return {
            'main': balance.main_balance,
            'frozen': balance.frozen_balance
        }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = User.objects.get(username=self.user.username)
        data.update({
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name
        })
        return data


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Example 1',
            value={
                "amount": 10.00,
                "description": "test uchun to'lov"
            },
            request_only=True  # Faqat so'rov uchun
        ),
        OpenApiExample(
            "Example 2",
            value={
                "amount": 100.00,
                "description": "Qoshimcha xizmatlar"
            },
            request_only=True
        )
    ]
)
class PaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01, message="To'lov miqdori 0 dan katta bo'lishi kerak"),
            # Qo'shimcha validatorlar...
        ]
    )

    description = serializers.CharField(max_length=255, required=False, help_text="To'lov haqida qo'shimcha ma'lumot")


