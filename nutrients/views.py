from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Nutrient
from .serializers import NutrientSerializer

# Create your views here.
class NutrientView(APIView):
  def get(self, request):
    try:
      room = Nutrient.objects.filter(username=request.user)
      serializer = NutrientSerializer(room, many=True).data
      return Response(serializer)
    except Nutrient.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)