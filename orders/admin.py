from django.contrib import admin
from .models import OrderModels, ClientModels, NanoModels, FeedBackModels


class OrderModelsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderModels._meta.fields]

    class Meta:
        model = OrderModels


admin.site.register(OrderModels, OrderModelsAdmin)


class ClientModelsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ClientModels._meta.fields]

    class Meta:
        model = ClientModels


admin.site.register(ClientModels, ClientModelsAdmin)


class NanoModelsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in NanoModels._meta.fields]

    class Meta:
        model = NanoModels


admin.site.register(NanoModels, NanoModelsAdmin)


class FeedBackModelsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FeedBackModels._meta.fields]

    class Meta:
            model = FeedBackModels


admin.site.register(FeedBackModels, FeedBackModelsAdmin)
