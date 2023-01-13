from django.urls import path, include
from . import views
from rest_framework import routers



urlpatterns = [
    path('update_gas', views.update_gas, name='update_gas'),
    path('update_electric', views.update_electric, name='update_electric'),
    path('update_weather', views.update_weather, name='update_weather'),
    path('generate_plot', views.generate_plot, name='generate_plot'),
    path('plots', views.PlotList.as_view(), name='list_plots'),
]