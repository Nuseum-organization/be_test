from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from dj_rest_auth.serializers import JWTSerializer
from django.conf import settings
from django.utils.module_loading import import_string
from django.contrib.auth import get_user_model
# TEST
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings
from multiprocessing import AuthenticationError
from datetime import datetime

class CustomRegisterSerializer(RegisterSerializer):

  def validate_username(self, username):
        codes = ['사과', '오이', '호박', '당근' , '시금치', '열무' , '토란', '감자', '브로콜리', '양배추', '비트', '테스트1', '테스트2', '테스트3', '테스트4', '테스트5'] # 30명 코드
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

# 로그인 response 처리
# Get the UserModel
UserModel = get_user_model()

class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """

    @staticmethod
    def validate_username(username):
        if 'allauth.account' not in settings.INSTALLED_APPS:
            # We don't need to call the all-auth
            # username validator unless its installed
            return username

        from allauth.account.adapter import get_adapter
        username = get_adapter().clean_username(username)
        return username

    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(UserModel, 'is_superuser'): # 추가
            extra_fields.append('is_superuser')
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)


class CustomJWTSerializer(JWTSerializer):
  """
  Serializer for JWT authentication.
  """
  access_token = serializers.CharField()
  refresh_token = serializers.CharField()
  user = serializers.SerializerMethodField()

  def get_user(self, obj):
      """
      Required to allow using custom USER_DETAILS_SERIALIZER in
      JWTSerializer. Defining it here to avoid circular imports
      """
      rest_auth_serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})

      JWTUserDetailsSerializer = import_string(
          rest_auth_serializers.get(
              'USER_DETAILS_SERIALIZER',
              # 'dj_rest_auth.serializers.UserDetailsSerializer',
              'accounts.serializers.UserDetailsSerializer',
          ),
      )

      user_data = JWTUserDetailsSerializer(obj['user'], context=self.context).data
      return user_data

# TEST
class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        print(f"SELF : {self.context['request'].COOKIES.get('my-app-auth')}")
        print(f"ATTRS : {attrs}")
        # 현재 저장된 access token expired time 확인
        token = self.context['request'].COOKIES.get('my-app-auth')
        if not token:
            raise AuthenticationError('UnAuthenticated!')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationError('UnAuthenticated!')
        print(payload['exp'])
        access_token_expired_time = datetime.fromtimestamp(payload['exp'])
        print(f"ACCESS EXP TIME : {access_token_expired_time}")

        now = datetime.now()
        print(f"NOW : {now}")

        print(f"CHECK : TIMEDELTA 사용해서 {now}와 {access_token_expired_time} 비교")
        print(f"ACCESS_EXP_TIME보다 NOW가 빠른가? {now < access_token_expired_time}")
                
        # TODO : IF로 비교해서 만료시간이 아직 안 되었으면 refresh token을 black list로 보냄
        refresh = self.token_class(attrs["refresh"])
        # 예외처리 : 비정상적인 처리
        if now < access_token_expired_time:
            # refresh 토큰 blacklist추가 == 강제 로그아웃
            try:
                # Attempt to blacklist the given refresh token
                refresh.blacklist()
            except AttributeError:
                # If blacklist app not installed, `blacklist` method will
                # not be present
                pass
            data = {
                'err_msg' : '비정상적인 토큰 발급입니다. 강제 로그아웃 되었습니다.'
            }
            return data

        # 만료 시간 이후에 발급받는 경우(정상적인 처리)
        data = {"access": str(refresh.access_token)}

        if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']:
            if settings.SIMPLE_JWT['BLACKLIST_AFTER_ROTATION']:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)

        return data