from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

# TEST(ViewSet)
# app_name = "posts"

# router = DefaultRouter()
# router.register("", views.PostViewSet)
# urlpatterns = router.urls

urlpatterns = [
  path('', views.PostView.as_view()),
]