# TODO : nutrient 계산 로직 구현
from foods.models import Food
import base64
import boto3
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

def day_calculate(day_food_data, day_water_data):
  
  # print(data) # 쿼리셋

  energy, protein, fat, carbohydrate, dietary_fiber, magnesium, vitamin_a, vitamin_d, vitamin_b6,\
  folic_acid, vitamin_b12, tryptophan, dha_epa = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
  # water_amount = 0

  for elem in day_food_data:

    food = Food.objects.get(id=elem['food_id'])
    # print(food, elem['amount'])
    energy += food.energy * (elem['amount'] / 100)
    protein += food.protein * (elem['amount'] / 100)
    fat += food.fat * (elem['amount'] / 100)
    carbohydrate += food.carbohydrate * (elem['amount'] / 100)
    dietary_fiber += food.dietary_fiber * (elem['amount'] / 100)
    magnesium += food.magnesium * (elem['amount'] / 100)
    vitamin_a += food.vitamin_a * (elem['amount'] / 100)
    vitamin_d += food.vitamin_d * (elem['amount'] / 100)
    vitamin_b6 += food.vitamin_b6 * (elem['amount'] / 100)
    folic_acid += food.folic_acid * (elem['amount'] / 100)
    vitamin_b12 += food.vitamin_b12 * (elem['amount'] / 100)
    tryptophan += food.tryptophan * (elem['amount'] / 100)
    dha_epa += food.dha_epa * (elem['amount'] / 100)

  # for elem in day_water_data:
  #   water_amount += elem['amount']
  
  sum_day_data = {
    'energy' : energy,
    'protein' : protein,
    'fat' : fat,
    'carbohydrate' : carbohydrate,
    'dietary_fiber' : dietary_fiber,
    'magnesium' : magnesium,
    'vitamin_a' : vitamin_a,
    'vitamin_d' : vitamin_d,
    'vitamin_b6' : vitamin_b6,
    'folic_acid' : folic_acid,
    'vitamin_b12' : vitamin_b12,
    'tryptophan' : tryptophan,
    'dha_epa' : dha_epa,
    'water_amount' : day_water_data.amount,
  }

  return sum_day_data


def week_month_calculate(week_data):

  total_energy, total_protein, total_fat, total_carbohydrate, total_dietary_fiber, total_magnesium, total_vitamin_a, total_vitamin_d, total_vitamin_b6,\
  total_folic_acid, total_vitamin_b12, total_tryptophan, total_dha_epa = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
  total_water = 0

  for elem in week_data: # queryset
    # print(elem.consumption_set.all())
    day_food_data = elem.consumption_set.all().values()
    day_water_data = elem.waterconsumption_set.all().get()
    # print(day_water_data)
    # print(day_data.values())
    sum_day_data = day_calculate(day_food_data, day_water_data)

    total_energy += sum_day_data['energy']
    total_protein += sum_day_data['protein']
    total_fat += sum_day_data['fat']
    total_carbohydrate += sum_day_data['carbohydrate']
    total_dietary_fiber += sum_day_data['dietary_fiber']
    total_magnesium += sum_day_data['magnesium']
    total_vitamin_a += sum_day_data['vitamin_a']
    total_vitamin_d += sum_day_data['vitamin_d']
    total_vitamin_b6 += sum_day_data['vitamin_b6']
    total_folic_acid += sum_day_data['folic_acid']
    total_vitamin_b12 += sum_day_data['vitamin_b12']
    total_tryptophan += sum_day_data['tryptophan']
    total_dha_epa += sum_day_data['dha_epa']
    total_water += sum_day_data['water_amount']

  sum_week_data = {
    'energy' : total_energy,
    'protein' : total_protein,
    'fat' : total_fat,
    'carbohydrate' : total_carbohydrate,
    'dietary_fiber' : total_dietary_fiber,
    'magnesium' : total_magnesium,
    'vitamin_a' : total_vitamin_a,
    'vitamin_d' : total_vitamin_d,
    'vitamin_b6' : total_vitamin_b6,
    'folic_acid' : total_folic_acid,
    'vitamin_b12' : total_vitamin_b12,
    'tryptophan' : total_tryptophan,
    'dha_epa' : total_dha_epa,
    'water_amount' : total_water,
  }

  return sum_week_data

def create_image_url(image_string, post_id, date_data, supplement_name, num):

  year = date_data.strftime('%Y')
  month = date_data.strftime('%m')
  day = date_data.strftime('%d')
  header, data = image_string.split(';base64,')
  # header, data = image_string[num].split(';base64,') # 리스트째로 들어옴!
  data_format, ext = header.split('/')
  try:
    image_data = base64.b64decode(data) # 이미지 파일 생성
    s3r = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    key = "%s"%(f'{year}/{month}/{day}')
    s3r.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(Key=key+'/%s'%(f'{post_id}_{supplement_name}_{num}.{ext}'), Body=image_data, ContentType='jpg')
    aws_url = f'{settings.IMAGE_URL}/{year}/{month}/{day}/{post_id}_{supplement_name}_{num}.{ext}'
    # FoodImage.objects.create(post=post, image=aws_url, meal_type=meal_type)

  except TypeError:
    data = {
      "err_msg" : "invalid_image"
    }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
  
  return aws_url

def delete_image(image_name):
  try:
    key = image_name.split('jinhyung.test.aws/')[1] # 파일명
    # print(key)
    s3_client = boto3.client(
      's3',
      aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
    
  except TypeError:
    data = {
      "err_msg" : "invalid_image"
    }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)