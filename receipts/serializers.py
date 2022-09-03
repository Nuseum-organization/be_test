from rest_framework import serializers
from .models import Receipt

class ReceiptSerializer(serializers.ModelSerializer):

  class Meta:
    model = Receipt
    fields = '__all__'

  def create(self, validated_data):
    receipt = Receipt.objects.create(**validated_data)
    return receipt