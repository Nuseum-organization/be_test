from dj_rest_auth.views import LoginView
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
# from dj_rest_auth import jwt_auth
from dj_rest_auth.serializers import JWTSerializerWithExpiration, TokenSerializer
from .serializers import CustomJWTSerializer

class CustomLoginView(LoginView):

  def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):

            if getattr(settings, 'JWT_AUTH_RETURN_EXPIRATION', False):
                response_serializer = JWTSerializerWithExpiration
            else:
                response_serializer = CustomJWTSerializer

        else:
            response_serializer = TokenSerializer
        return response_serializer

  def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_simplejwt.settings import (
                api_settings as jwt_settings,
            )
            access_token_expiration = (timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME)
            refresh_token_expiration = (timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME)
            return_expiration_times = getattr(settings, 'JWT_AUTH_RETURN_EXPIRATION', False)
            auth_httponly = getattr(settings, 'JWT_AUTH_HTTPONLY', False)

            data = {
                'user': self.user,
                'access_token': self.access_token,
            }
            # print(data['user'].is_superuser)

            if not auth_httponly:
                data['refresh_token'] = self.refresh_token
            else:
                # Wasnt sure if the serializer needed this
                data['refresh_token'] = ""

            if return_expiration_times:
                data['access_token_expiration'] = access_token_expiration
                data['refresh_token_expiration'] = refresh_token_expiration

            serializer = serializer_class(
                instance=data,
                context=self.get_serializer_context(),
            )
        elif self.token:
            serializer = serializer_class(
                instance=self.token,
                context=self.get_serializer_context(),
            )
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

        response = Response(serializer.data, status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            from dj_rest_auth.jwt_auth import set_jwt_cookies
            # set_jwt_cookies(response, self.access_token, self.refresh_token)
            custom_set_jwt_cookies(response, self.access_token, self.refresh_token)
        return response

def custom_set_jwt_cookies(response, access_token, refresh_token):
    custom_set_jwt_access_cookie(response, access_token)
    custom_set_jwt_refresh_cookie(response, refresh_token)

def custom_set_jwt_access_cookie(response, access_token):
    from config.settings import SIMPLE_JWT as jwt_settings
    cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
    access_token_expiration = (timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME)
    cookie_secure = getattr(settings, 'JWT_AUTH_SECURE', False)
    cookie_httponly = getattr(settings, 'JWT_AUTH_HTTPONLY', True)
    # cookie_samesite = getattr(settings, 'JWT_AUTH_SAMESITE', 'Lax')
    cookie_samesite = getattr(settings, 'JWT_AUTH_SAMESITE', None)

    if cookie_name:
        response.set_cookie(
            cookie_name,
            access_token,
            expires=access_token_expiration,
            secure=cookie_secure,
            httponly=cookie_httponly,
            samesite=cookie_samesite,
        )


def custom_set_jwt_refresh_cookie(response, refresh_token):
    from config.settings import SIMPLE_JWT as jwt_settings
    refresh_token_expiration = (timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME)
    refresh_cookie_name = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE', None)
    refresh_cookie_path = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE_PATH', '/')
    cookie_secure = getattr(settings, 'JWT_AUTH_SECURE', False)
    cookie_httponly = getattr(settings, 'JWT_AUTH_HTTPONLY', True)
    # cookie_samesite = getattr(settings, 'JWT_AUTH_SAMESITE', 'Lax')
    cookie_samesite = getattr(settings, 'JWT_AUTH_SAMESITE', None)

    if refresh_cookie_name:
        response.set_cookie(
            refresh_cookie_name,
            refresh_token,
            expires=refresh_token_expiration,
            secure=cookie_secure,
            httponly=cookie_httponly,
            samesite=cookie_samesite,
            path=refresh_cookie_path,
        )