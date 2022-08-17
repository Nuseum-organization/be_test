from rest_framework import serializers
from .models import Post
from foods.models import Food, Category
from foods.serializers import FoodSerializer
from nutrients.serializers import NutrientSerializer
from nutrients.models import Nutrient
from .calculates import calculate
from datetime import date



class PostSerializer(serializers.ModelSerializer):
  
  def get_or_create_foods(self, foods):
      food_ids = []
      for food in foods:
          food_instance, created = Food.objects.get_or_create(pk=food.get('id'), defaults=food)
          food_ids.append(food_instance.pk)
      return food_ids
  
  class Meta:
    model = Post
    # fields = '__all__'
    exclude = ('author',)

  def create(self, validated_data): # post 생성 (이때 음식에 amount 추가 필요)

    # 각 식단의 음식별 섭취량 추출
    if validated_data['breakfast_amount'] == '[]':
      breakfast_amount = [0.0]
    else:
      breakfast_amount = list(map(float, validated_data['breakfast_amount'][1:-1].split(',')))

    if validated_data['lunch_amount'] == '[]':
      lunch_amount = [0.0]
    else:
      lunch_amount = list(map(float, validated_data['lunch_amount'][1:-1].split(',')))

    if validated_data['dinner_amount'] == '[]':
      dinner_amount = [0.0]
    else:
      dinner_amount = list(map(float, validated_data['dinner_amount'][1:-1].split(',')))

    if validated_data['snack_amount'] == '[]':
      snack_amount = [0.0]
    else:
      snack_amount = list(map(float, validated_data['snack_amount'][1:-1].split(',')))

    if validated_data['supplement_amount'] == '[]':
      supplement_amount = [0.0]
    else:
      supplement_amount = list(map(float, validated_data['supplement_amount'][1:-1].split(',')))

    result = [0] * 13
    # c_result = set()
    category_result = Category.objects.none() # 빈 쿼리셋 생성
    breakfast = validated_data.pop('breakfast', [])
    # print(breakfast)
    result, category_result = calculate(breakfast, breakfast_amount, result, category_result)

    lunch = validated_data.pop('lunch', [])
    result, category_result = calculate(lunch, lunch_amount, result, category_result)

    dinner = validated_data.pop('dinner', [])
    result, category_result = calculate(dinner, dinner_amount, result, category_result)

    snack = validated_data.pop('snack', [])
    result, category_result = calculate(snack, snack_amount, result, category_result)

    supplement = validated_data.pop('supplement', [])
    result, category_result = calculate(supplement, supplement_amount, result, category_result)
    # print(result, c_result)
 
    # NutrientSerializer 사용하면 되지 않나? -> 테스트 필요!
    nutrient = Nutrient.objects.create( # 하루 영양정보 생성
      username=validated_data['author'], 
      energy = result[0],
      carbohydrate = result[1],
      protein = result[2],
      fat = result[3],
      dietary_fiber = result[4],
      magnesium = result[5],
      vitamin_a = result[6],
      vitamin_d = result[7],
      vitamin_b6 = result[8],
      vitamin_b12 = result[9],
      folic_acid = result[10],
      tryptophan = result[11],
      dha_epa = result[12],
      # created_at = date.today()
      created_at = validated_data['created_at'] # 임시 설정
    )
    # 오늘 먹은 음식들의 카테고리 기록
    categories_id = []
    for elem in category_result:
      categories_id.append(elem[0])
    nutrient.category.set(categories_id)

    post = Post.objects.create(**validated_data)
    post.breakfast.set(breakfast)
    post.lunch.set(lunch)
    post.dinner.set(dinner)
    post.snack.set(snack)
    post.supplement.set(supplement)
    post.created_at = validated_data['created_at']
    return post

  # def update(self, instance, validated_data):
  #   # 우선 validated_data에서 가져오기 (-> 지금은 입력받지 않으면 기존 값이 입력되도록 한 것인가? : 체크 필요!)
  #   # instance.breakfast = validated_data.get("breakfast", instance.breakfast) # 값이 없는 경우 default 값(instance.field == 현재값)
  #   # instance.lunch = validated_data.get("lunch", instance.lunch)
  #   # instance.dinner = validated_data.get("dinner", instance.dinner)
  #   # instance.snack = validated_data.get("snack", instance.snack)
  #   # instance.supplement = validated_data.get("supplement", instance.supplement)
    
  #   # print(validated_data)
  #   # print(validated_data.get("breakfast", instance.breakfast))
  #   # print(instance.breakfast)
  #   instance.breakfast.set(validated_data.get("breakfast", instance.breakfast)) # 값이 없는 경우 default 값(instance.field == 현재값)
  #   instance.lunch.set(validated_data.get("lunch", instance.lunch))
  #   instance.dinner.set(validated_data.get("dinner", instance.dinner))
  #   instance.snack.set(validated_data.get("snack", instance.snack))
  #   instance.supplement.set(validated_data.get("supplement", instance.supplement))
  #   instance.breakfast_amount = validated_data.get("breakfast_amount", instance.breakfast_amount)
  #   instance.lunch_amount = validated_data.get("lunch_amount", instance.lunch_amount)
  #   instance.dinner_amount = validated_data.get("dinner_amount", instance.dinner_amount)
  #   instance.snack_amount = validated_data.get("snack_amount", instance.snack_amount)
  #   instance.supplement_amount = validated_data.get("supplement_amount", instance.supplement_amount)
  #   instance.pic1 = validated_data.get("pic1", instance.pic1)
  #   instance.pic2 = validated_data.get("pic2", instance.pic2)
  #   instance.pic3 = validated_data.get("pic3", instance.pic3)

    instance.save()
    return instance # 항상 instance를 return해야 함
