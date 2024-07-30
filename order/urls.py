from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet


urlpatterns = [
    path('order/', OrderViewSet.as_view()),
]