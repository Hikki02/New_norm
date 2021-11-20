
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    ReportSerializer, ExcelFileSerializer, ExcelFileTemplatesSerializer,
    AddProductToExcelFileSerializer, UserSerializer)
from .models import Report, ExcelFile, ExcelFileTemplate, AddProductToExcelFile
from users.models import User

from datetime import datetime
import os


class ExcelFileTemplatesViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = ExcelFileTemplate.objects.all()
    serializer_class = ExcelFileTemplatesSerializer

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ExcelFileViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = ExcelFile.objects.all()
    serializer_class = ExcelFileSerializer

    def list(self, request, *args, **kwargs):
        file = self.queryset.filter(user=self.request.user)
        serializer = self.serializer_class(file, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        id_file = serializer.initial_data['id']
        name_file = ExcelFile.objects.get(id=id_file).excel_file
        os.remove('/home/xxxx/unnamed_project_v3/media/' + str(name_file))
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReportViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def list(self, request, *args, **kwargs):
        print(request.data)
        report = self.queryset.filter(user=self.request.user)
        serializer = self.serializer_class(report, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def check_on_num(request_read):
    full_url = str(request_read)
    id_exel_file = ''
    for i in range(4, 11):
        if full_url[-i].isdigit() is True:
            id_exel_file += full_url[-i]
        else:
            break
    return id_exel_file[::-1]


class ReportListView(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def list(self, request, *args, **kwargs):
        exel_file = check_on_num(request.read)
        report = self.queryset.filter(excel_file=exel_file)
        serializer = self.serializer_class(report, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddProductToExcelFileViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = AddProductToExcelFile.objects.all()
    serializer_class = AddProductToExcelFileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        for i, j in serializer.data.items():
            print(f"{str(i)}" + ": " + f"{str(j)}")
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendDataViewSet(ModelViewSet):
    queryset = ExcelFile.objects.all()
    serializer_class = ExcelFileSerializer
    http_method_names = ['post', 'get']

    def create(self, request, *args, **kwargs):
        """Обновляет is_order на True из-за чего он отправляется на админку"""
        serializer = self.serializer_class(request.data)
        is_order = serializer.data['is_order']
        exel_id = serializer.data['id']
        ExcelFile.objects.filter(id=exel_id).update(is_order=is_order, date_send=datetime.now())
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """Показывает данные User который отправил Excel файлы"""
        queryset = User.objects.get(id=request.GET['user_id'])
        serializer = UserSerializer(queryset)
        return Response(serializer.data)


class OrderSendRoomViewSet(ModelViewSet):
    queryset = ExcelFile.objects.filter(is_order=True)
    serializer_class = ExcelFileSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        """Отдает Excel файлы у которых is_order=True, в комнату администратора"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

