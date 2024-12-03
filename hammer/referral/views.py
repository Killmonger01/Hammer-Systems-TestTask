from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import View
from rest_framework.response import Response
from rest_framework import status
from api.models import User, InviteRelation


class registration_page(View):
    def get(self, request):
        return render(request, 'register.html')
        
    def post(self, request):
        """Логин пользователя после проверки кода"""
        phone_number = request.POST.get('phone_number')

        # Проверяем, существует ли пользователь
        user = User.objects.filter(phone_number=phone_number).first()
        if user:
            # Логиним пользователя
            login(request, user)
            # Перенаправляем на страницу профиля
            return redirect('referral:profile')
        
        # Если пользователь не найден, возвращаем ошибку
        return render(request, 'register.html', {'error': 'Пользователь не найден'})



def profile(request):
    return render(request, 'profile.html')

def index(request):
    return redirect('referral:register')

