import time
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User, InviteRelation
from .serializers import PhoneAuthSerializer, CodeAuthSerializer, ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Моделируем хранение кодов авторизации
auth_codes = {}

class PhoneAuthView(APIView):
    def post(self, request):
        """Запрос на ввод номера телефона и генерацию 4-значного кода"""
        serializer = PhoneAuthSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            # Проверка, есть ли пользователь в базе данных
            
            # Генерация и сохранение кода
            code = str(random.randint(1000, 9999))
            auth_codes[phone_number] = code

            # Имитация отправки кода с задержкой
            time.sleep(2)  # Задержка 2 секунды
            print(f"Отправлен код: {code}")

            detail_message = f"Код: {code}"
            
            return Response({"detail": detail_message}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeAuthView(APIView):
    def post(self, request):
        """Проверка кода и авторизация пользователя"""
        serializer = CodeAuthSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']

            # Проверка правильности кода
            if auth_codes.get(phone_number) == code:
                user, created = User.objects.get_or_create(phone_number=phone_number)
                if created:
                    user.generate_invite_code()  # Генерация инвайт-кода при первой авторизации
                
                # Генерация JWT токенов
                refresh = RefreshToken.for_user(user)
                return Response({
                    "detail": "Авторизация успешна",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }, status=status.HTTP_200_OK)
            
            return Response({"detail": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProfileView(APIView):
    def get(self, request):
        """Получение профиля пользователя"""
        if not request.user.is_authenticated:
            return Response({"detail": "Вы не аутентифицированы"}, status=status.HTTP_401_UNAUTHORIZED)

        user = get_object_or_404(User, phone_number=request.user.phone_number)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        """Активация инвайт-кода"""
        print(4)
        print("Request Data:", request.data)
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('user_number')
            print(phone_number)
            print(123)

            # Получаем текущего пользователя
            user = get_object_or_404(User, phone_number=phone_number)
            activated_invite_code = request.data.get('activated_invite_code')

            # Проверяем инвайт-код
            inviter = User.objects.filter(invite_code=activated_invite_code).first()
            print(user)
            print(inviter)
            if not inviter or inviter == user:
                return Response({"detail": "Недействительный инвайт-код"}, status=status.HTTP_400_BAD_REQUEST)

            # Проверяем, активирован ли уже инвайт-код
            if user.activated_invite_code:
                return Response({"detail": "Инвайт-код уже активирован"}, status=status.HTTP_400_BAD_REQUEST)

            # Активируем инвайт-код
            user.activated_invite_code = activated_invite_code
            user.save()

            return Response({"detail": "Инвайт-код активирован"}, status=status.HTTP_200_OK)
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
