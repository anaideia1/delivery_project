from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.users.views import UserViewSet
from api.orders.views import OrderViewSet


router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
