from django.test import TestCase
from energy_tracker.models import Historical_Gas, Predictions
from datetime import datetime
from api.views import current_date

class HistoricalGasTestClass(TestCase):
    def create_historical_gas(self):
        date = current_date()
        consumption = 10

        return Historical_Gas.objects.create(
            date=date,
            consumption=consumption
        )

    def test_historical_gas_creation(self):
        obj = self.create_historical_gas()
        self.assertTrue(isinstance(obj, Historical_Gas))
        self.assertEqual(str(obj), f'{obj.date}: {obj.consumption} - created: {obj.created}')


class PredictionsTestClass(TestCase):
    def create_prediction(self):
        y_pred = [1,2,3,4,5,6,7]
        obj =  Predictions.objects.create(
            energy_type = 1,
            sum_predicted_usage = sum(y_pred)
        )
        obj.set_predicted_usage(y_pred)

        return obj

    def test_prediction_creation(self):
        obj = self.create_prediction()
        self.assertTrue(isinstance(obj, Predictions))
        self.assertEqual(obj.sum_predicted_usage, 28)
        self.assertEqual(obj.predicted_usage, '[1, 2, 3, 4, 5, 6, 7]')
        self.assertEqual(obj.get_predicted_usage(), [1, 2, 3, 4, 5, 6, 7])



