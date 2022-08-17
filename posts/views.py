from django.shortcuts import render
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from nutrients.serializers import NutrientSerializer
import json, time
from datetime import datetime

# TEST
# class PostViewSet(ModelViewSet):
#   queryset = Post.objects.all()
#   serializer_class = PostSerializer

#   def get_queryset(self):
#     return super().get_queryset().filter(author=self.request.user)

class PostView(APIView): # admin에서 추가할 경우 serializer를 사용하지 않고 추가하기 때문에 Nutrient가 생성되지 않음!

  # pk로 해당 post 가져오는 함수
  def get_post(self, request, date):
    try:
      # post = Post.objects.get(author=self.request.user)
      print(self.request.user)
      post = Post.objects.get(author=self.request.user, created_at=date)
      print(post.created_at)
      print(type(post.created_at))
      return post
    except Post.DoesNotExist:
      return None

  def get_post_by_id(self, pk):
    try:
      post = Post.objects.get(pk=pk)
      return post
    except Post.DoesNotExist:
      return None

  # post 테스트 시 주석처리 필요
  def get(self, request):
    date = self.request.GET.get('date', None)
    if date is None: # 존재하지 않는 날짜 쿼리 시 예외처리
      return Response(status=status.HTTP_404_NOT_FOUND)
    # date 변환
    date = datetime.fromtimestamp(int(date)/1000).strftime("%Y%m%d")
    post = self.get_post(self, date)
    # print(post)
    if post is not None:
      serializer = PostSerializer(post).data
      return Response(serializer)
    else:
      return Response(status=status.HTTP_404_NOT_FOUND)

  # TODO : POST LIST 추가 필요 ** -> mypage에서만 보여줄지 고민중임!

  # serializer에 update 메서드 추가 필요 -> (주의) put시 하루 영양성분을 다시 계산하는 로직도 구현 필요***
  def put(self, request, pk): # pk는 post.id (GET으로 프론트에서 post.id를 우선 받고, PUT메서드를 보낼 때 URL에 pk를 보내주어야 함!)
    post = self.get_post_by_id(pk)
    print(post)
    print(post.lunch)
    print(post.dinner)
    if post is not None:
      if post.author != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)
      
      serializer = PostSerializer(post, data=request.data, partial=True)
      print(serializer.is_valid(), serializer.errors) # True {}
      if serializer.is_valid():
        post = serializer.save() # serializer의 update 메서드 호출
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

    # convert datetime format of unix timestamp string(1660575600000) -> string(20220816)
    request.data['created_at'] = datetime.fromtimestamp(int(request.data['created_at'])/1000).strftime("%Y%m%d")
    # print(type(datetime.fromtimestamp(request.data['created_at']/1000)))
    
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

