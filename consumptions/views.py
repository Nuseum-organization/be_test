from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import Consumption, WaterConsumption, SupplementConsmption, FoodImage
from .serializers import SupplementDetailSerializer
from .utils import *
from posts.models import Post
from accounts.models import User
from receipts.models import Receipt

# 하루동안 영양소 총합을 보여주는 VIEW
class DayNutrientView(APIView):
  
  def get_post(self, request, date):
    try:
      post = Post.objects.get(author=self.request.user, created_at=date)
      return post
    except Post.DoesNotExist:
      return None

  def get(self, request):
    date = self.request.GET.get('date', None)
    # 존재하지 않는 날짜 쿼리 시 예외처리
    if date is None:
      data = {
        'error_msg' : '올바른 날짜를 입력하세요.'
      }
      return Response(status=status.HTTP_404_NOT_FOUND, data=data)
    # Date Format 변환
    date = datetime.fromtimestamp(int(date)/1000)
    post = self.get_post(self, date)
    if post is not None:
      # 음식 정보
      food_consumptions = Consumption.objects.filter(post=post.id)
      # 물 정보
      water_consumption = WaterConsumption.objects.get(post=post.id)
      # Queryset to JSON
      day_food_data = food_consumptions.values() # <class 'django.db.models.query.QuerySet'>
      day_water_data = water_consumption # 가져오는 값은 한개뿐임
      # print(day_water_data)
      # calculate logic
      sum_day_data = day_calculate(day_food_data, day_water_data)
      return Response(data=sum_day_data) 
    else:
      data = {
        'error_msg' : '해당 날짜에 작성된 포스트가 존재하지 않습니다.'
      }
      return Response(status=status.HTTP_404_NOT_FOUND, data=data)

# 일주일동안 영양소 총합을 보여주는 View
class WeekNutrientView(APIView):

  def get_all_posts(self, request, date):
    today_date = datetime.fromtimestamp(int(date)/1000)
    a_week_ago = datetime.fromtimestamp((int(date) - 518400000)/1000)
    try:
      post = Post.objects.filter(author=self.request.user, created_at__lte=today_date, created_at__gte=a_week_ago).order_by('created_at')
      return post
    except Post.DoesNotExist:
      return None

  def get(self, request):
    date = self.request.GET.get('date', None)
    # 존재하지 않는 날짜 쿼리 시 예외처리
    if date is None:
      data = {
        'error_msg' : '올바른 날짜를 입력하세요.'
      }
      return Response(status=status.HTTP_404_NOT_FOUND, data=data)
    posts = self.get_all_posts(self, date)
    sum_week_data = week_month_calculate(posts) # 쿼리셋 전달 -> 함수 내에서 개별 개체에 대해 역참조!
    # 날짜 출력 확인
    # for elem in posts:
    #   print(elem)
    return Response(data=sum_week_data)

# 한달동안 영양소 총합을 보여주는 View
class MonthNutrientView(APIView):

  def get_all_posts(self, request, date):
    today_date = datetime.fromtimestamp(int(date)/1000)
    a_month_ago = datetime.fromtimestamp((int(date) - 2592000000)/1000)
    try:
      post = Post.objects.filter(author=self.request.user, created_at__lte=today_date, created_at__gte=a_month_ago).order_by('created_at')
      return post
    except Post.DoesNotExist:
      return None

  def get(self, request):
    date = self.request.GET.get('date', None)
    # 존재하지 않는 날짜 쿼리 시 예외처리
    if date is None:
      data = {
        'error_msg' : '올바른 날짜를 입력하세요.'
      }
      return Response(status=status.HTTP_404_NOT_FOUND, data=data)
    posts = self.get_all_posts(self, date)
    sum_month_data = week_month_calculate(posts) # 쿼리셋 전달 -> 함수 내에서 개별 개체에 대해 역참조!
    # 날짜 출력 확인
    # for elem in posts:
    #   print(elem)
    return Response(data=sum_month_data)

# 관리자 페이지 뷰 -> 유저가 사용하는 API가 아니기 때문에 다소 복잡해도 크게 문제되지는 않을듯!
class AdminView(APIView):

  # 필요시 권한설정 추가
  # permission_classes = []

  def get_post(self, request, author, date):
    if date is None: # date 입력값이 없으면 모두 출력
      try:
        user = User.objects.get(username=author) # author 없는 경우 예외처리 **
        posts = Post.objects.filter(author=user.id).order_by('created_at') # 날짜별로 오름차순으로 정렬?
        return posts
      except Post.DoesNotExist:
        return None
      except User.DoesNotExist:
        return None
    else:
      try:
        # print(author)
        # print(date)
        date = datetime.fromtimestamp(int(date)/1000)
        user = User.objects.get(username=author)
        post = Post.objects.filter(author=user.id, created_at=date)
        return post
      except Post.DoesNotExist:
        return None
      except User.DoesNotExist:
        return None

  def get(self, request):
    author = self.request.GET.get('author', None) 
    date = self.request.GET.get('date', None)
    posts = self.get_post(self, author, date)
    # 유저가 존재하지 않으면 posts는 None -> posts.exists() 사용 불가
    if posts is not None:
      # 유저는 존재하지만 게시글이 없으면 posts는 Queryset<[]> -> posts.exists()를 사용하여 에러 처리 가능
      if not posts.exists():
        data = {
          'error_msg' : '입력한 유저가 해당 날짜에 작성한 포스트가 없습니다.'
        }
        return Response(status=status.HTTP_404_NOT_FOUND, data=data)

      # print(posts)
      admin_data = {}
      for elem in posts: # posts 개수만큼 반복하면서 날짜별로 기록
        # print(elem)
        # elem에는 post.id와 created_at이 존재함
        post_id = elem.id
        date = elem.created_at
        # post_id = elem.values('id')
        # date = elem.values('created_at')
        print(post_id, date)
        breakfast_consumptions = Consumption.objects.filter(post=post_id, meal_type='breakfast')
        breakfast_images = FoodImage.objects.filter(post=post_id, meal_type='breakfast')
        breakfast_images_queryset = breakfast_images.values('image')
        breakfast_images_list = []
        for i in range(len(breakfast_images_queryset)):
          breakfast_images_list.append(breakfast_images_queryset[i]['image'])

        lunch_consumptions = Consumption.objects.filter(post=post_id, meal_type='lunch')
        lunch_images = FoodImage.objects.filter(post=post_id, meal_type='lunch')
        lunch_images_queryset = lunch_images.values('image')
        lunch_images_list = []
        for i in range(len(lunch_images_queryset)):
          lunch_images_list.append(lunch_images_queryset[i]['image'])
        
        dinner_consumptions = Consumption.objects.filter(post=post_id, meal_type='dinner')
        dinner_images = FoodImage.objects.filter(post=post_id, meal_type='dinner')
        dinner_images_queryset = dinner_images.values('image')
        dinner_images_list = []
        for i in range(len(dinner_images_queryset)):
          dinner_images_list.append(dinner_images_queryset[i]['image'])
        
        snack_consumptions = Consumption.objects.filter(post=post_id, meal_type='snack')
        snack_images = FoodImage.objects.filter(post=post_id, meal_type='snack')
        snack_images_queryset = snack_images.values('image')
        snack_images_list = []
        for i in range(len(snack_images_queryset)):
          snack_images_list.append(snack_images_queryset[i]['image'])

        water_consumption = WaterConsumption.objects.get(post=post_id)
        supplement_consumption = SupplementConsmption.objects.filter(post=post_id)
        supplements = SupplementDetailSerializer(instance=supplement_consumption, many=True)
        # 영수증 정보 추가
        receipts = Receipt.objects.filter(post=post_id) # queryset이므로 values()로 내보내야 함!
        
        temp_data = {
          'breakfast' : {
            'data' : breakfast_consumptions.values(),
            'image' : breakfast_images_list,
          },
          'lunch' : {
            'data' : lunch_consumptions.values(),
            'image' : lunch_images_list,
          },
          'dinner' : {
            'data' : dinner_consumptions.values(),
            'image' : dinner_images_list,
          },
          'snack' : {
            'data' : snack_consumptions.values(),
            'image' : snack_images_list,
          },
          'water' : water_consumption.amount,
          'supplement' : supplements.data,
          'receipt' : receipts.values(), 
        }
        admin_data[str(date).split(' ')[0]] = temp_data

      return Response(data=admin_data)
    # 유저가 존재하지 않으면 posts는 None -> posts.exists() 사용 불가
    else:
      data = {
        'error_msg' : '해당 유저가 존재하지 않습니다.'
      }
      return Response(status=status.HTTP_404_NOT_FOUND, data=data)