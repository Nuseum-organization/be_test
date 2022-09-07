from django.urls import path
from . import views

urlpatterns = [
  path('day/', views.DayNutrientView.as_view()),
  path('week/', views.WeekNutrientView.as_view()),
  path('month/', views.MonthNutrientView.as_view()),
  # 오늘탭 뷰
  path('today/', views.TodayView.as_view()),
  # 관리자 페이지 뷰
  path('admin/', views.AdminView.as_view()),
]