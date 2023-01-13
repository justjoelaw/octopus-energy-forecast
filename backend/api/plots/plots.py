import pandas as pd
import numpy as np
import seaborn as sns
import sqlite3
import matplotlib.pyplot as plt
import os
from django.conf import settings
from energy_tracker.models import *
from api.regression.regression import create_regression_model
from datetime import datetime, timedelta
import pandas as pd




# Helper functions

def format_historical_data(days_ago):

    df_weather = pd.DataFrame(list(Historical_Weather.objects.all().order_by('-date')[:days_ago].values('date', 'avg_temperature')))
    df_gas = pd.DataFrame(list(Historical_Gas.objects.all().order_by('-date')[:days_ago].values('date', 'consumption')))
    df_electric = pd.DataFrame(list(Historical_Electric.objects.all().order_by('-date')[:days_ago].values('date', 'consumption')))

    merged = pd.merge(df_weather, df_gas, on=['date'], suffixes=['_weather', '_gas'])
    merged = pd.merge(merged, df_electric, on=['date'], suffixes=['_gas', '_electric'])

    return merged



# Plots
def create_gas_plot(days_ago=60):
    historical_data = format_historical_data(days_ago)

    fig, ax = plt.subplots()
    ax.plot(historical_data.date, historical_data.avg_temperature, 'r', label='temp')
    ax2 = ax.twinx()
    ax2.plot(historical_data.date, historical_data.consumption_gas, 'b', label='gas')

    ax.set(ylabel='Avg Daily temperature (C)')
    ax2.set(ylabel='Daily Gas Consumption (m^3)')

    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=315)

    ax.legend(loc=2)
    ax2.legend(loc=1)
    ax.grid(axis = 'x')

    return fig

def create_electric_plot(days_ago=60):
    historical_data = format_historical_data(days_ago)

    fig, ax = plt.subplots()
    ax.plot(historical_data.date, historical_data.avg_temperature, 'r', label='temp')
    ax2 = ax.twinx()
    ax2.plot(historical_data.date, historical_data.consumption_electric, 'b', label='electric')

    ax.set(ylabel='Avg Daily temperature (C)')
    ax2.set(ylabel='Daily Electricity Consumption (kWh)')

    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=315)

    ax.legend(loc=2)
    ax2.legend(loc=1)
    ax.grid(axis = 'x')

    return fig

def create_regression_plot(weather_week, days_ago=60, energy_type='gas'):
    historical_data = format_historical_data(days_ago)

    regressor = create_regression_model(historical_data, energy_type)

    df_weather_week = pd.DataFrame(weather_week, columns = ['date', 'avg_temperature'])
    df_weather_week['date'] = pd.to_datetime(df_weather_week['date'])
    df_weather_week['day_of_week'] = df_weather_week['date'].dt.day_name()

    df_dummies = pd.get_dummies(df_weather_week)
    X_week = df_dummies[['avg_temperature', 'day_of_week_Friday',
        'day_of_week_Monday', 'day_of_week_Saturday', 'day_of_week_Sunday',
            'day_of_week_Thursday', 'day_of_week_Tuesday', 'day_of_week_Wednesday']]
    y_pred = regressor.predict(X_week)

    fig, ax = plt.subplots()
    ax.plot(df_weather_week.date, df_weather_week.avg_temperature, 'r', label='temp')
    ax2 = ax.twinx()
    ax2.plot(df_weather_week.date, y_pred, 'b', label=energy_type)

    ax.set(ylabel='Forecast Avg Daily temperature (C)')
    if energy_type=='gas':
        ax2.set(ylabel='Predicted Daily Gas Consumption (m^3)')
    elif energy_type=='electric':
        ax2.set(ylabel='Predicted Daily Electricity Consumption (kWh)')

    ax.xaxis.set_major_locator(plt.MaxNLocator(7))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=315)

    ax.legend(loc=2)
    ax2.legend(loc=1)
    
    ax.grid(axis = 'x')

    return fig, y_pred

