from django.urls import path, include
from rest_framework import routers

from .views import *
app_name = 'orders'

router = routers.DefaultRouter()
router.register('safe_order_and_send_email', OrderSafeAndSendEmailViewSet, basename='safe_order_and_send_email')
router.register('phone',  OrderSafeAndSendClientViewSet, basename='phone')
router.register('nano', OrderSafeAndSendNanoViewSet, basename='nano')
router.register('feed-back', OrderSafeAndSendFeedBackViewSet, basename='feedback')

urlpatterns = [
    path('', include(router.urls))
]
