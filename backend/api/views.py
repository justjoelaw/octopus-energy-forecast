import sys
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import environ
from .octopus_api_functions.octopus_api_functions import get_gas, get_electric
from energy_tracker.models import Historical_Electric, Historical_Gas, Historical_Weather, Historical_Plots, Predictions
from django.shortcuts import HttpResponse
from datetime import timedelta, datetime
from .plots.plots import create_gas_plot, create_electric_plot, create_regression_plot
from datetime import datetime
import io
from django.core.files import File
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from rest_framework import generics
from .serializers import PlotSerializer, PredictionSerializer, GasSerializer, ElectricSerializer
from django.db.models import Q
from django.http import JsonResponse


# Import environment variables
env = environ.Env()
environ.Env.read_env()

# Helper functions:

def current_date():
    now = datetime.now()
    return now.strftime("%Y-%m-%d")

def date_range(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    date_list = []
    delta = timedelta(days=1)
    while start <= end:
        date_list.append(start.strftime("%Y-%m-%d"))
        start += delta
    return date_list


def get_weather_history(date):

    url = 'http://api.weatherapi.com/v1/history.json'

    params = {
    'key': env('WEATHER_API_KEY'),
    'q': env('WEATHER_LOCATION'),
    'dt': date
    }

    r = requests.get(url, params=params)

    if r.status_code != 200:
        raise ValueError(f'Request failed with status code {r.status_code}')

    return r.json()

def get_weather_forecast(days=8):

    url = 'http://api.weatherapi.com/v1/forecast.json'

    params = {
    'key': env('WEATHER_API_KEY'),
    'q': env('WEATHER_LOCATION'),
    'days': days
    }

    r = requests.get(url, params=params)

    if r.status_code != 200:
        raise ValueError(f'Request failed with status code {r.status_code}')

    return r.json()

def get_weather_week():
    output_list = []

    weather_json = get_weather_forecast()

    for forecast_day in weather_json['forecast']['forecastday'][1:]: # Exclude today from forecast
        date = forecast_day['date']
        date_avg_temp = forecast_day['day']['avgtemp_c']
        output_list.append([date, date_avg_temp])

    return output_list


# API Views

@api_view(['POST'])
def update_gas(request):
    if request.method == 'POST':

        date_today = current_date()

        try:
            from_date = request.data['from_date']
        except KeyError:
            from_date = datetime.strptime(date_today, "%Y-%m-%d") - timedelta(days=61)
        try:
            to_date = request.data['to_date']
        except KeyError:
            to_date = datetime.strptime(date_today, "%Y-%m-%d") - timedelta(days=2)

        gas_json = get_gas(from_date, to_date)
        created_records = 0

        for result in gas_json['results']:
            date = result['interval_start'].split('T')[0]
            consumption = result['consumption']
            try:
                historical_gas = Historical_Gas.objects.get(date=date)
                historical_gas.consumption = consumption
                historical_gas.save()
            except Historical_Gas.DoesNotExist:
                historical_gas = Historical_Gas.objects.create(date=date, consumption=consumption)
                created_records += 1

        return HttpResponse(f'Created {created_records} records in the Historical_gas table')

        
@api_view(['POST'])
def update_electric(request):
    if request.method == 'POST':
        date_today = current_date()

        try:
            from_date = request.data['from_date']
        except KeyError:
            from_date = datetime.strptime(date_today, "%Y-%m-%d") - timedelta(days=61)
        try:
            to_date = request.data['to_date']
        except KeyError:
            to_date = datetime.strptime(date_today, "%Y-%m-%d") - timedelta(days=2)

        print(from_date, to_date)
        electric_json = get_electric(from_date, to_date)
        created_records = 0

        print(len(electric_json['results']))

        for result in electric_json['results']:
            date = result['interval_start'].split('T')[0]
            consumption = result['consumption']
            try:
                historical_electric = Historical_Electric.objects.get(date=date)
                historical_electric.consumption = consumption
                historical_electric.save()
            except Historical_Electric.DoesNotExist:
                historical_electric = Historical_Electric.objects.create(date=date, consumption=consumption)
                created_records += 1

        return HttpResponse(f'Created {created_records} records in the Historical_electric table')


@api_view(['POST'])
def update_weather(request):
    if request.method == 'POST':
        
        date_today = current_date()

        try:
            from_date = request.data['from_date']
        except KeyError:
            from_date = (datetime.strptime(date_today, "%Y-%m-%d") - timedelta(days=61)).strftime("%Y-%m-%d")
        try:
            to_date = request.data['to_date']
        except KeyError:
            to_date = (datetime.strptime(date_today, "%Y-%m-%d") - timedelta(days=2)).strftime("%Y-%m-%d")


        date_list = date_range(from_date, to_date)

        created_records = 0

        for date in date_list:
            weather_json = get_weather_history(date)
            date_avg_temp = weather_json['forecast']['forecastday'][0]['day']['avgtemp_c']
            print(date, date_avg_temp)

            historical_weather, created = Historical_Weather.objects.get_or_create(
                date = date,
                avg_temperature = date_avg_temp
                )

            if created:
                created_records += 1

        return HttpResponse(f'Created {created_records} records in the Historical_weather table')


@api_view(['POST'])
def generate_plot(request):
    plot_type_enum = {
        'gas': 1,
        'electric': 2,
        'temperature': 3,
        'prediction': 4
    }

    energy_type_enum = {
        'gas': 1,
        'electric': 2
    }

    if request.method == 'POST':
        plot_type = request.data['plot_type']
        try:
            prediction_on = request.data['prediction_on']
        except KeyError:
            prediction_on = None

        if plot_type == 'gas':
            fig = create_gas_plot()
        elif plot_type == 'electric':
            fig = create_electric_plot()
        elif plot_type == 'prediction':
            weather_week = get_weather_week()
            fig, y_pred = create_regression_plot(weather_week, energy_type=prediction_on)
        else:
            return HttpResponse("Invalid plot_type. Allowed values are: ['gas','electric', 'prediction']", status=400)


        date = current_date()
        prediction = None

        # Save the plot to a buffer
        buf = io.BytesIO()
        fig.savefig(buf, bbox_inches='tight')
        buf.seek(0)

        # Create a File object
        if prediction_on:
            file = File(buf, name=f'{plot_type}_{prediction_on}_{date}.png')

            prediction = Predictions.objects.create(
                energy_type = energy_type_enum[prediction_on],
                sum_predicted_usage = sum(y_pred.tolist())
            )
            prediction.set_predicted_usage(y_pred.tolist())
            prediction.save()

        else:
            file = File(buf, name=f'{plot_type}_{date}.png')


        historical_plot, created = Historical_Plots.objects.get_or_create(
            date = date,
            image = file,
            plot_type = plot_type_enum[plot_type]
        )

        if created:
            return JsonResponse({
                'msg': 'Created new plot',
                'plot_id': historical_plot.id,
                'plot': PlotSerializer(historical_plot, context={'request': request}).data,
                'prediction_id': prediction.id if prediction else '',
                'prediction': PredictionSerializer(prediction, context={'request': request}).data if prediction else {}

            })
        else:
            return HttpResponse('Plot was not created', status=400)


class PlotList(generics.ListAPIView):
    model = Historical_Plots
    serializer_class = PlotSerializer

    def get_queryset(self):
        latest_only = bool(self.request.query_params.get('latest_only'))

        if latest_only:
            q1 = Historical_Plots.objects.filter(date=current_date(), plot_type=1)
            q2 = Historical_Plots.objects.filter(date=current_date(), plot_type=2)

            if len(q1) == 0:
                q1_id = -1 # Will not exist
            else:
                q1_id = q1.latest('created').id

            if len(q2) == 0:
                q2_id = -1 # Will not exist
            else:
                q2_id = q2.latest('created').id

            queryset = Historical_Plots.objects.filter(pk__in=[q1_id, q2_id])
        else:
            queryset = Historical_Plots.objects.all()
            
        return queryset

        
class HistoricGasList(generics.ListAPIView):
    model = Historical_Gas
    serializer_class = GasSerializer

    def get_queryset(self):
        queryset = Historical_Gas.objects.all().order_by('-date')[:60]
        return queryset

class HistoricElectricList(generics.ListAPIView):
    model = Historical_Electric
    serializer_class = ElectricSerializer

    def get_queryset(self):
        queryset = Historical_Electric.objects.all().order_by('-date')[:60]
        return queryset