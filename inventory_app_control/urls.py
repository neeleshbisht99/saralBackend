from django.urls import path, include
from .views import (
    FoodItemViewSet, OrderViewSet
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)


router.register('food-items', FoodItemViewSet, "food-item")
router.register('orders', OrderViewSet, "order")

urlpatterns = [
    path("", include(router.urls))
]