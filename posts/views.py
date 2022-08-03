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

  def post(self, request):
    b_amount, l_amount, d_amount, s_amount = [], [] ,[] ,[]
    print(request.data)
    for i in range(len(request.data['breakfast'])):
      b_amount.append(request.data['breakfast'][i][1])
      request.data['breakfast'][i] = request.data['breakfast'][i][0]

    for i in range(len(request.data['lunch'])):
      l_amount.append(request.data['lunch'][i][1])
      request.data['lunch'][i] = request.data['lunch'][i][0]

    for i in range(len(request.data['dinner'])):
      d_amount.append(request.data['dinner'][i][1])
      request.data['dinner'][i] = request.data['dinner'][i][0]

    for i in range(len(request.data['snack'])):
      s_amount.append(request.data['snack'][i][1])
      request.data['snack'][i] = request.data['snack'][i][0]
    
    print(b_amount)
    print(l_amount)
    print(d_amount)
    print(s_amount)

    serializer = PostSerializer(data=request.data)
    # print(request.data['breakfast'])
    # print()
    # print(serializer)
    if serializer.is_valid():
      post = serializer.save(author=request.user, b_amount=str(b_amount), l_amount=str(l_amount), d_amount=str(d_amount), s_amount=str(s_amount))
      post_serializer = PostSerializer(post).data
      print(post_serializer)
      return Response(data=post_serializer, status=status.HTTP_200_OK)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

