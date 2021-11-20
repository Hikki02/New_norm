from django.urls import include, path
from rest_framework import routers

from .views import (
    ReportViewSet, ExcelFileViewSet, ReportListView, ExcelFileTemplatesViewSet,
    AddProductToExcelFileViewSet, SendDataViewSet, OrderSendRoomViewSet
)

router = routers.DefaultRouter()
router.register('reports-list', ReportViewSet)
router.register('excel', ExcelFileViewSet)
router.register('excel-templates', ExcelFileTemplatesViewSet)
router.register('add-product', AddProductToExcelFileViewSet)
router.register('send', SendDataViewSet)
router.register('room', OrderSendRoomViewSet)
router.register('reports-list-filter', ReportListView)


urlpatterns = [
    path('', include(router.urls)),
]
