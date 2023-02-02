from django.test import TestCase
from api.octopus_api_functions.octopus_api_functions import get_gas, get_electric
from django.utils import timezone
from api.views import current_date, update_gas, update_electric, update_weather, get_weather_week, get_weather_history, PlotList, generate_plot
from api.plots.plots import format_historical_data, create_gas_plot, create_electric_plot, create_regression_plot
from datetime import datetime, timedelta
from rest_framework.test import APIRequestFactory
from energy_tracker.models import Historical_Gas, Historical_Electric, Historical_Weather, Historical_Plots, Predictions
from api.regression.regression import create_regression_model


class GasAPITest(TestCase):
    def gas_api_call(self, from_date, to_date):
        gas_json = get_gas(from_date, to_date)

        return gas_json

    def gas_api_call_fail(self):
        gas_json = get_gas('x', 'y')

        return gas_json

    def test_gas_api_fail(self):
        self.assertRaises(ValueError, self.gas_api_call_fail)

    def test_gas_api(self):
        date_today = current_date()
        from_date = datetime.strptime(date_today, "%Y-%m-%d") - timedelta(days=61)
        to_date = datetime.strptime(date_today, "%Y-%m-%d") - timedelta(days=2)

        gas_json = self.gas_api_call(from_date, to_date)
        results = gas_json['results']
        self.assertEqual(len(results), 60)


class ElectricAPITest(TestCase):
    def electric_api_call(self, from_date, to_date):
        electric_json = get_electric(from_date, to_date)

        return electric_json

    def electric_api_call_fail(self):
        electric_json = get_electric('x', 'y')

        return electric_json

    def test_electric_api_fail(self):
        self.assertRaises(ValueError, self.electric_api_call_fail)

    def test_electric_api(self):
        date_today = current_date()
        from_date = datetime.strptime(date_today, "%Y-%m-%d") - timedelta(days=61)
        to_date = datetime.strptime(date_today, "%Y-%m-%d") - timedelta(days=2)

        electric_json = self.electric_api_call(from_date, to_date)
        results = electric_json['results']
        self.assertEqual(len(results), 60)

class WeatherAPITests(TestCase):
    
    date_today = current_date()

    def test_get_weather_history(self):
        weather_json = get_weather_history(self.date_today)
        date_avg_temp = weather_json['forecast']['forecastday'][0]['day']['avgtemp_c']
        self.assertGreater(date_avg_temp, -100)
        self.assertLess(date_avg_temp, 100)

    def test_get_weather_history_fail(self):
        self.assertRaises(ValueError, get_weather_history, 'x')



class ExistingDataTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        factory = APIRequestFactory()

        # Update gas
        request = factory.post('/update_gas')
        update_gas(request)

        # Update Electric
        request = factory.post('/update_electric')
        update_electric(request)

        # Update Weather
        request = factory.post('/update_weather')
        update_weather(request)

        # Update Forecast
        get_weather_week()

    def test_historical_gas_update(self):
        self.assertEqual(Historical_Gas.objects.all().count(), 60)

    def test_historical_electric_update(self):
        self.assertEqual(Historical_Electric.objects.all().count(), 60)

    def test_historical_weather_update(self):
        self.assertEqual(Historical_Weather.objects.all().count(), 60)

    def test_format_historical_data(self):
        merged = format_historical_data(7)
        self.assertEqual(len(merged.index), 7)

    def test_create_gas_plot(self):
        fig = create_gas_plot()
        self.assertIsNotNone(fig)

    def test_create_electric_plot(self):
        fig = create_electric_plot()
        self.assertIsNotNone(fig)

    def test_create_prediction_plot(self):
        fig = create_electric_plot()
        self.assertIsNotNone(fig)

    def test_create_regression_plot(self):
        weather_week = get_weather_week()
        fig, y_pred = create_regression_plot(weather_week)
        self.assertIsNotNone(fig)
        self.assertEqual(len(y_pred), 7)

    def test_create_regressor(self):
        historical_data = format_historical_data(60)

        regressor = create_regression_model(historical_data, 'gas')
        self.assertIsNotNone(regressor)

        regressor = create_regression_model(historical_data, 'electric')
        self.assertIsNotNone(regressor)

    def test_plot_list(self):
        factory = APIRequestFactory()

        request = factory.post('/generate_plot', {
            'plot_type': 'gas'
        })
        generate_plot(request)

        request = factory.post('/generate_plot', {
            'plot_type': 'electric'
        })
        generate_plot(request)

        request = factory.get('plots?latest_only=True')
        view = PlotList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_generate_plot_regression(self):
        factory = APIRequestFactory()

        request = factory.post('/generate_plot', {
            'plot_type': 'prediction',
            'prediction_on': 'gas'
        })
        generate_plot(request)

        request = factory.post('/generate_plot', {
            'plot_type': 'prediction',
            'prediction_on': 'electric'
        })
        generate_plot(request)

        self.assertEqual(Historical_Plots.objects.filter(plot_type=4).count(), 2)
        self.assertEqual(Predictions.objects.filter(energy_type=1).count(), 1)
        self.assertEqual(Predictions.objects.filter(energy_type=2).count(), 1)
