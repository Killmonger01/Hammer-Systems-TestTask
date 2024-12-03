from django.urls import path
from . import views
from api.views import ProfileView

app_name = 'referral'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registration_page.as_view(), name='register'),
    path('profile/', views.profile, name='profile'),
]
