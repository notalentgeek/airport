from django.contrib import admin
from .models import AirTrafficController, Arrival, Departure

# Register your models here.
admin.site.register(Arrival)
admin.site.register(Departure)
admin.site.register(AirTrafficController)