from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Historical_Gas)
admin.site.register(Historical_Electric)
admin.site.register(Historical_Plots)
admin.site.register(Historical_Weather)
admin.site.register(Predictions)