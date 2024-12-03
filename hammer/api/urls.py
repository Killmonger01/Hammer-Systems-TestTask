from django.urls import path
from .views import PhoneAuthView, CodeAuthView, ProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'api'

urlpatterns = [
    path('auth/phone/', PhoneAuthView.as_view(), name='phone_auth'),
    path('auth/code/', CodeAuthView.as_view(), name='code_auth'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
