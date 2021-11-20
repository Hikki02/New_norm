from rest_framework import serializers

from users.models import User
from .models import (
    Report, ExcelFile, ExcelFileTemplate, AddProductToExcelFile
)


class ExcelFileTemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFileTemplate
        fields = '__all__'


class ExcelFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFile
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class ReportReadableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class AddProductToExcelFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddProductToExcelFile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'email', )
