from django.urls import path
from . import views

urlpatterns = [
  path('', views.ReceiptCreateAPIView.as_view()),
  path('<int:pk>/', views.ReceiptDetailAPIView.as_view()),
  path('<int:pk>/delete/', views.ReceiptDeleteAPIView.as_view()),
  path('list/', views.ReceiptListAPIView.as_view()),
]