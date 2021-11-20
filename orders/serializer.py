from rest_framework import serializers
from .models import OrderModels, ClientModels, NanoModels, FeedBackModels


class OrderModelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderModels
        fields = '__all__'


class ClientModelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientModels
        fields = '__all__'


class NanoModelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = NanoModels
        fields = '__all__'


class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBackModels
        fields = '__all__'
