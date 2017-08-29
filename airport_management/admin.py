from django.contrib import admin
from .models import AirTrafficController, ArrivalFlight, DepartureFlight, Lane

class DepartureArrival(admin.ModelAdmin):
    list_display = (
        "flight_code",
        "airport",
        "day",
        "sch_local_datetime",
        "carrier",
        "lane",
        "online_atc",
        "past_atcs",
        "proper_atc"
    )
    list_filter = ["sch_local_datetime"]

# Register your models here.
admin.site.register(Lane)
admin.site.register(ArrivalFlight, DepartureArrival)
admin.site.register(DepartureFlight, DepartureArrival)
admin.site.register(AirTrafficController)