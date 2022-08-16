from django.shortcuts import render
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from nutrients.serializers import NutrientSerializer
import json

# TEST
# class PostViewSet(ModelViewSet):
#   queryset = Post.objects.all()
#   serializer_class = PostSerializer

#   def get_queryset(self):
#     return super().get_queryset().filter(author=self.request.user)

class PostView(APIView): # admin에서 추가할 경우 serializer를 사용하지 않고 추가하기 때문에 Nutrient가 생성되지 않음!

  # pk로 해당 post 가져오는 함수
  def get_post(self, request, pk):
    try:
      post = Post.objects.get(pk=pk)
      return post
    except Post.DoesNotExist:
      return None

  # post 하나만 가져오기 -> 굳이 이럴 필요 없이, 해당 유저가 쓴 글 전체를 가져오는 것이 더 효과적인가?
  # def get(self, request, pk):
  #   post = self.get_post(self, pk)
  #   if post is not None:
  #     serializer = PostSerializer(post).data
  #     return Response(serializer)
  #   else:
  #     return Response(status=status.HTTP_404_NOT_FOUND)

  # TODO : POST LIST 추가 필요 ** -> mypage에서만 보여줄지 고민중임!

  # serializer에 update 메서드 추가 필요 -> (주의) put시 하루 영양성분을 다시 계산하는 로직도 구현 필요***
  def put(self, request, pk):
    post = self.get_post(pk)
    if post is not None:
      if post.author != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)
      
      serializer = PostSerializer(post, data=request.data, partial=True)
      print(serializer.is_valid(), serializer.errors)
      if serializer.is_valid():
        post = serializer.save()
        return Response(PostSerializer(post).data)
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQEUST)
      return Response()
    else:
      return Response(status=status.HTTP_404_NOT_FOUND)

  def post(self, request):
    breakfast_amount, lunch_amount, dinner_amount, snack_amount, supplement_amount = [], [] ,[] ,[], []
    # print(request.data)
    
    breakfast_length = len(request.data['breakfast'])
    for i in range(breakfast_length):
      breakfast_amount.append(request.data['breakfast'][i][1])
      request.data['breakfast'][i] = request.data['breakfast'][i][0]

    lunch_length = len(request.data['lunch'])
    for i in range(lunch_length):
      lunch_amount.append(request.data['lunch'][i][1])
      request.data['lunch'][i] = request.data['lunch'][i][0]

    dinner_length = len(request.data['dinner'])
    for i in range(dinner_length):
      dinner_amount.append(request.data['dinner'][i][1])
      request.data['dinner'][i] = request.data['dinner'][i][0]

    snack_length = len(request.data['snack'])
    for i in range(snack_length):
      snack_amount.append(request.data['snack'][i][1])
      request.data['snack'][i] = request.data['snack'][i][0]

    supplement_length = len(request.data['supplement'])
    for i in range(supplement_length):
      supplement_amount.append(request.data['supplement'][i][1])
      request.data['supplement'][i] = request.data['supplement'][i][0]
    
    # print(breakfast_amount)
    # print(lunch_amount)
    # print(dinner_amount)
    # print(snack_amount)
    # print(supplement_amount)

    serializer = PostSerializer(data=request.data)
    # print(request.data['breakfast'])
    # print()
    # print(serializer)
    if serializer.is_valid():
      post = serializer.save(
        author=request.user, 
        breakfast_amount=str(breakfast_amount), 
        lunch_amount=str(lunch_amount), 
        dinner_amount=str(dinner_amount), 
        snack_amount=str(snack_amount),
        supplement_amount = str(supplement_amount)
      )
      post_serializer = PostSerializer(post).data
      print(post_serializer)
      return Response(data=post_serializer, status=status.HTTP_200_OK)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

