from django.contrib import admin
from .models import DailySalesReport, WeeklySalesReport, MonthlySalesReport

admin.site.register(DailySalesReport)
admin.site.register(WeeklySalesReport)
admin.site.register(MonthlySalesReport)
