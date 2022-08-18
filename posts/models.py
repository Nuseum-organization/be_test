from django.db import models
from accounts.models import User
from foods.models import Food

class Post(models.Model):
  # title = models.CharField(max_length=30) # title 삭제
  author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
  
  # consumption
  breakfast = models.ManyToManyField(Food, blank=True, related_name='breakfast_food')
  lunch = models.ManyToManyField(Food, blank=True, related_name='lunch_food')
  dinner = models.ManyToManyField(Food, blank=True, related_name='dinner_food')
  snack = models.ManyToManyField(Food, blank=True, related_name='snack_food')
  # supplement = models.ManyToManyField(Food, blank=True, related_name='supplement_food') # 영양제 정보 추가
  breakfast_amount = models.CharField(max_length=100, blank=True, null=True)
  lunch_amount = models.CharField(max_length=100, blank=True, null=True)
  dinner_amount = models.CharField(max_length=100, blank=True, null=True)
  snack_amount = models.CharField(max_length=100, blank=True, null=True)
  # supplement_amount=  models.CharField(max_length=100, blank=True, null=True) # 영양제 정보 추가
  
  # remark = models.TextField()
  # comment = models.Textfield() 

  # image 따로 빼서 관리
  breakfast_img = models.ImageField(upload_to='post/images/%Y/%m/%d', blank=True)
  lunch_img = models.ImageField(upload_to='post/images/%Y/%m/%d', blank=True)
  dinner_img = models.ImageField(upload_to='post/images/%Y/%m/%d', blank=True)
  snack_img = models.ImageField(upload_to='post/images/%Y/%m/%d', blank=True)
  
  # created_at = models.DateTimeField()
  created_at = models.CharField(max_length=10) # string 필드로 변경
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'[{self.pk}] {self.author}\'s post :: {self.created_at}'
    # return f'[{self.pk}]{self.title} :: {self.author}'