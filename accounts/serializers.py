from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from django.utils.translation import gettext_lazy as _
from accounts.models import User

class CustomRegisterSerializer(RegisterSerializer):

  def validate_username(self, username):
        codes = ['사과', '오이', '호박', '당근' , '시금치', '열무' , '토란', '감자', '브로콜리', '양배추'] # 30명 코드
        username = get_adapter().clean_username(username)
        if username not in codes:
          raise serializers.ValidationError(_("올바른 코드를 입력하세요!"))
        return username

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'is_superuser']

class UserListSerializer(serializers.Serializer):
  userList = UserSerializer(many=True)
