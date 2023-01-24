from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Historical_Gas)
class HistoricalGasAdmin(admin.ModelAdmin):
    list_display = ('date', 'consumption', 'created')

@admin.register(Historical_Electric)
class HistoricalElectricAdmin(admin.ModelAdmin):
    list_display = ('date', 'consumption', 'created')

@admin.register(Historical_Weather)
class HistoricalWeatherAdmin(admin.ModelAdmin):
    list_display = ('date', 'avg_temperature', 'created')

@admin.register(Historical_Plots)
class HistoricalPlotsAdmin(admin.ModelAdmin):
    list_display = ('date', 'image', 'created')

@admin.register(Predictions)
class PredictionsAdmin(admin.ModelAdmin):
    list_display = ('created', 'predicted_usage', 'sum_predicted_usage')