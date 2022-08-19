def calculate(meal, amount,  result, category_result):
  # result = [0] * 13 # 12개 index
  for i in range(len(meal)):
  # for m in meal:
    result[0] += meal[i].energy * (amount[i] / 100)
    result[1] += meal[i].carbohydrate * (amount[i]  / 100)
    result[2] += meal[i].protein * (amount[i] / 100)
    result[3] += meal[i].fat * (amount[i] / 100)
    result[4] += meal[i].dietary_fiber * (amount[i] / 100)
    result[5] += meal[i].magnesium * (amount[i] / 100)
    result[6] += meal[i].vitamin_a * (amount[i] / 100)
    result[7] += meal[i].vitamin_d * (amount[i] / 100)
    result[8] += meal[i].vitamin_b6 * (amount[i] / 100)
    result[9] += meal[i].vitamin_b12 * (amount[i] / 100)
    result[10] += meal[i].folic_acid * (amount[i] / 100)
    result[11] += meal[i].tryptophan * (amount[i] / 100)
    result[12] += meal[i].dha_epa * (amount[i] / 100)
    # 카테고리 추가
    category_result |= meal[i].category.values_list()
  return result, category_result

# string amount(validated_data) -> float amount(list) 
def extract_amount_from_validated(validated_data, meal_amount):
  if validated_data[meal_amount] == '[]':
    meal_amount = [0.0]
  else:
    meal_amount = list(map(float, validated_data[meal_amount][1:-1].split(',')))
  return meal_amount

# string amount(list) -> float amount(list)
def extract_amount_from_list(meal_amount):
  tmp_list = meal_amount[1:-1].split(',')
  if tmp_list[0] == '':
    tmp_list = [0.0]
  else:
    tmp_list = list(map(float, tmp_list))
  return tmp_list