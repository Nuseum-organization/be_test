from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.views import UserDetailsView
from .serializers import CustomDetailSerializer
from .models import User
from posts.models import Post
from posts.serializers import PostSerializer

class CustomDetailView(UserDetailsView):

  serializer_class = CustomDetailSerializer
  permission_classes = (IsAuthenticated,)

# [feat] 마이페이지를 들어가면 작성한 post 목록을 보여줌 -> 현 상황에서 필요할까?
# class MyPostView(APIView):
#   def get(self, request):
#     try:
#       post = Post.objects.filter(author=request.user)
#       serializer = PostSerializer(post, many=True).data
#       return Response(serializer)
#     except Post.DoesNotExist:
#       return Response(status=status.HTTP_404_NOT_FOUND)

# for test
# class UserSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = User
#     fields = '__all__'

# class UserViewSet(viewsets.ModelViewSet):
#   queryset = User.objects.all()
#   serializer_class = UserSerializer

