from rest_framework.permissions import AllowAny

from .models import User, UserBalance, Transaction
from .serializers import PaymentSerializer
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer


class UserListCreateView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    # 1. GET - Barcha user larni olish
    def get(self, request):
        user = User.objects.all()
        serializer = self.serializer_class(user, many=True)
        return Response(serializer.data)

    # 2. POST - Yangi user yaratish

    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer},
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                user = serializer.save()
                UserBalance.objects.create(user=user)
                return Response({
                    'status': 'success',
                    'new_balance': user.username
                }, status=status.HTTP_200_OK)


        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserDestroyUpdatePatchDeleteAPIView(APIView):
    serializer_class = UserSerializer
    # 1. GET - Bitta user ni olish
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    # 2. PUT - To'liq yangilash (barcha maydonlar talab qilinadi)
    @extend_schema(
        request=UserSerializer,  # PUT yoki PATCH uchun ham serializer ko'rsatilishi kerak
        responses={200: UserSerializer},
    )
    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = self.serializer_class(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # 3. PATCH - Qisman yangilash (faqat berilgan maydonlar yangilanadi)
    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = self.serializer_class(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # 4. DELETE - Userni o'chirish
    def delete(self, request, user_id):
        article = User.objects.get(pk=user_id)
        article.delete()
        return Response(status=204)  # 204 No Content


class PaymentView(APIView):
    serializer_class = PaymentSerializer
    @extend_schema(
        request=PaymentSerializer,
        responses={
            200: PaymentSerializer,
            400: {"description": "Invalid input"},
            404: {"description": "User balance not found"}
        },
    )
    async def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                # Balansni yangilash
                user_balance = UserBalance.objects.select_for_update().only(
                    'main_balance'
                ).get(user_id=request.user.id)
                user_balance.main_balance += serializer.validated_data['amount']
                user_balance.save(update_fields=['main_balance'])

                # Tranzaksiyani yaratish
                Transaction.objects.create(
                    user=request.user,
                    amount=serializer.validated_data['amount'],
                    transaction_type='deposit',
                    status='completed',
                    details={
                        'description': serializer.validated_data.get('description', ''),
                        'source': 'api_payment'
                    }
                )

                return Response({
                    'status': 'success',
                    'new_balance': user_balance.main_balance
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
