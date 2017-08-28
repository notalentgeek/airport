from django.contrib import admin
from .models import AirTrafficController, ArrivalFlight, DepartureFlight, Lane

# Register your models here.
admin.site.register(Lane)
admin.site.register(ArrivalFlight)
admin.site.register(DepartureFlight)
admin.site.register(AirTrafficController)