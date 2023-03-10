from energy_tracker.models import Historical_Electric, Historical_Gas, Historical_Weather, Historical_Plots, Predictions
from rest_framework import serializers

class PlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historical_Plots
        fields = '__all__'

class GasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historical_Gas
        fields = '__all__'

class ElectricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historical_Electric
        fields = '__all__'

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predictions
        fields = '__all__'