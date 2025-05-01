from django.urls import path
from .views import PaymentView,UserListCreateView, UserDestroyUpdatePatchDeleteAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = 'user'
urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-create'),  # POST, List
    path('users/<int:user_id>/', UserDestroyUpdatePatchDeleteAPIView.as_view(), name='user-detail'),  # GET, PUT, PATCH, DELETE
    path('payment/', PaymentView.as_view(), name='make-payment'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]