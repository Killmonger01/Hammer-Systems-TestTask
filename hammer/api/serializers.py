from rest_framework import serializers
from .models import User, InviteRelation
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed

class PhoneAuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

class CodeAuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=4)

class ProfileSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()
    user_number = serializers.CharField()

    class Meta:
        model = User
        fields = ['user_number', 'invite_code', 'activated_invite_code', 'invited_users']

    def get_invited_users(self, obj):
        return [relation.invitee.phone_number for relation in obj.invited_users.all()]
    

