from rest_framework import serializers
from .models import Nutrient

class NutrientSerializer(serializers.ModelSerializer):

  created_at = serializers.DateTimeField(format="%Y-%m-%d")
  updated_at = serializers.DateTimeField(format="%Y-%m-%d")

  class Meta:
    model = Nutrient
    fields = '__all__'

  def create(self, validated_data):
    request = self.context.get('request')
    nutrient = Nutrient.objects.create(**validated_data, user=request.user)
    return nutrient