from traceback import extract_tb
from rest_framework import serializers
from .models import Post
from foods.models import Food, Category
from foods.serializers import FoodSerializer
from nutrients.serializers import NutrientSerializer
from nutrients.models import Nutrient
from .utils import *
from datetime import date

# Food.id와 Food.name로 출력을 표현하는 Serializer
# 리팩토링 때 적용! (나중에 사용)
# ModelSerializer를 사용해야 class Meta가 적용됨!
class NameSerializer(serializers.ModelSerializer):

  breakfast = serializers.StringRelatedField(many=True)
  lunch = serializers.StringRelatedField(many=True)
  dinner = serializers.StringRelatedField(many=True)
  snack = serializers.StringRelatedField(many=True)

  class Meta:
    model = Post
    # fields = '__all__'
    exclude = ('author',)


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

    # 1.각 식단의 음식별 섭취량 추출(extract amount) : String -> float
    breakfast_amount = extract_amount_from_validated(validated_data, 'breakfast_amount')
    lunch_amount = extract_amount_from_validated(validated_data, 'lunch_amount')
    dinner_amount = extract_amount_from_validated(validated_data, 'dinner_amount')
    snack_amount = extract_amount_from_validated(validated_data, 'snack_amount')
    supplement_amount = extract_amount_from_validated(validated_data, 'supplement_amount')

    # if validated_data['breakfast_amount'] == '[]':
    #   breakfast_amount = [0.0]
    # else:
    #   breakfast_amount = list(map(float, validated_data['breakfast_amount'][1:-1].split(',')))

    # if validated_data['lunch_amount'] == '[]':
    #   lunch_amount = [0.0]
    # else:
    #   lunch_amount = list(map(float, validated_data['lunch_amount'][1:-1].split(',')))

    # if validated_data['dinner_amount'] == '[]':
    #   dinner_amount = [0.0]
    # else:
    #   dinner_amount = list(map(float, validated_data['dinner_amount'][1:-1].split(',')))

    # if validated_data['snack_amount'] == '[]':
    #   snack_amount = [0.0]
    # else:
    #   snack_amount = list(map(float, validated_data['snack_amount'][1:-1].split(',')))

    # if validated_data['supplement_amount'] == '[]':
    #   supplement_amount = [0.0]
    # else:
    #   supplement_amount = list(map(float, validated_data['supplement_amount'][1:-1].split(',')))

    # 2.영양소 계산 및 카테고리 추출(calculate nutrient & extract category)
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
    # print(result, category_result)
 
    # 3.Nutrient 객체 생성(create Nutrient instance)
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
    # 카테고리 저장 (오늘 먹은 음식들의 카테고리 기록)
    categories_id = []
    for elem in category_result:
      categories_id.append(elem[0])
    nutrient.category.set(categories_id)

    # 4. Post 객체 생성(create Post instance)
    post = Post.objects.create(**validated_data)
    post.breakfast.set(breakfast)
    post.lunch.set(lunch)
    post.dinner.set(dinner)
    post.snack.set(snack)
    post.supplement.set(supplement)
    post.created_at = validated_data['created_at']
    return post

  def update(self, instance, validated_data):
    print(validated_data)
    # post update
    # set을 하면서 순서가 사라져버림....ㄷㄷㄷㄷ
    instance.breakfast.set(validated_data.get("breakfast", [])) # 값이 없는 경우 default 값(instance.field == 현재값)
    # print(instance.breakfast)
    instance.lunch.set(validated_data.get("lunch", []))
    instance.dinner.set(validated_data.get("dinner", []))
    instance.snack.set(validated_data.get("snack", []))
    instance.supplement.set(validated_data.get("supplement", []))
    instance.breakfast_amount = validated_data.get("breakfast_amount", "[]")
    instance.lunch_amount = validated_data.get("lunch_amount", "[]")
    instance.dinner_amount = validated_data.get("dinner_amount", "[]")
    instance.snack_amount = validated_data.get("snack_amount", "[]")
    instance.supplement_amount = validated_data.get("supplement_amount", "[]")
    instance.breakfast_img1 = validated_data.get("breakfast_img1", '')
    instance.breakfast_img2 = validated_data.get("breakfast_img2", '')
    instance.breakfast_img3 = validated_data.get("breakfast_img3", '')
    instance.lunch_img1 = validated_data.get("lunch_img1", '')
    instance.lunch_img2 = validated_data.get("lunch_img2", '')
    instance.lunch_img3 = validated_data.get("lunch_img3", '')
    instance.dinner_img1 = validated_data.get("dinner_img1", '')
    instance.dinner_img2 = validated_data.get("dinner_img2", '')
    instance.dinner_img3 = validated_data.get("dinner_img3", '')
    instance.snack_img1 = validated_data.get("snack_img1", '')
    instance.snack_img2 = validated_data.get("snack_img2", '')
    instance.snack_img3 = validated_data.get("snack_img3", '')
    instance.save()

    # nutrient update
    # - 해당 인스턴스의 날짜와 작성자와 일치하는 Nutrient 객체를 찾아서 우선 get해오고
    # - 다시 계산된 값(result)의 각 필드를 가져와서 Nutrient 객체의 값 필드에 할당함

    # result of newly calculated data
    breakfast_amount = extract_amount_from_list(instance.breakfast_amount)
    lunch_amount = extract_amount_from_list(instance.lunch_amount)
    dinner_amount = extract_amount_from_list(instance.dinner_amount)
    snack_amount = extract_amount_from_list(instance.snack_amount)
    supplement_amount = extract_amount_from_list(instance.supplement_amount)

    result = [0] * 13
    category_result = Category.objects.none() # 빈 쿼리셋 생성
    breakfast = instance.breakfast.all()
    # print(breakfast.all())
    result, category_result = calculate(breakfast, breakfast_amount, result, category_result)

    lunch = instance.lunch.all()
    result, category_result = calculate(lunch, lunch_amount, result, category_result)

    dinner = instance.dinner.all()
    result, category_result = calculate(dinner, dinner_amount, result, category_result)

    snack = instance.snack.all()
    result, category_result = calculate(snack, snack_amount, result, category_result)

    supplement = instance.supplement.all()
    result, category_result = calculate(supplement, supplement_amount, result, category_result)

    # 카테고리 저장 (오늘 먹은 음식들의 카테고리 기록)
    categories_id = []
    for elem in category_result:
      categories_id.append(elem[0])
    # nutrient.category.set(categories_id)

    nutrient = Nutrient.objects.get(username=instance.author, created_at=instance.created_at)
    print(nutrient)
    # 가져온 nutrient에 새로 계산된 값들 할당 후 저장
    nutrient.energy = result[0]
    nutrient.carbohydrate = result[1]
    nutrient.protein = result[2]
    nutrient.fat = result[3]
    nutrient.dietary_fiber = result[4]
    nutrient.magnesium = result[5]
    nutrient.vitamin_a = result[6]
    nutrient.vitamin_d = result[7]
    nutrient.vitamin_b6 = result[8]
    nutrient.vitamin_b12 = result[9]
    nutrient.folic_acid = result[10]
    nutrient.tryptophan = result[11]
    nutrient.dha_epa = result[12]
    nutrient.category.set(Category.objects.none()) # 카테고리는 한번 비운 후 재할당
    nutrient.category.set(categories_id)
    nutrient.save() # 저장

    return instance # 항상 instance를 return해야 함
