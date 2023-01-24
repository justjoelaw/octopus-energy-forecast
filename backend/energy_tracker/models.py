from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import json

# Create your models here.

class Historical_Gas(models.Model):
    date = models.DateField(unique=True)
    consumption = models.FloatField(validators=[MinValueValidator(0.0)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.date}: {self.consumption} - created: {self.created}'

class Historical_Electric(models.Model):
    date = models.DateField(unique=True)
    consumption = models.FloatField(validators=[MinValueValidator(0.0)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Historical_Weather(models.Model):
    date = models.DateField(unique=True)
    avg_temperature = models.FloatField(validators=[MinValueValidator(0.0)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Historical_Plots(models.Model):
    date = models.DateField()
    image = models.ImageField(upload_to='images/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Plot_Type(models.IntegerChoices):
        GAS = 1, 'Gas'
        ELECTRIC = 2, 'Electric'
        TEMPERATURE = 3, 'Temperature'
        PREDICTION = 4, 'Prediction'

    plot_type = models.IntegerField(choices=Plot_Type.choices)

class Predictions(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    predicted_usage = models.CharField(max_length=1000)
    sum_predicted_usage = models.FloatField()

    def set_predicted_usage(self, lst):
        self.predicted_usage = json.dumps(lst)

    def get_predicted_usage(self):
        return json.loads(self.predicted_usage)


    class Energy_Type(models.IntegerChoices):
        GAS = 1, 'Gas'
        ELECTRIC = 2, 'Electric'
    energy_type = models.IntegerField(choices=Energy_Type.choices)