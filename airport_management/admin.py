from django.contrib import admin
from .models import AirTrafficController, ArrivalFlight, DepartureFlight, Lane

class ArrivalDeparture(admin.ModelAdmin):
    list_display = (
        "pk",
        "flight_code",
        "airport",
        "day",
        "sch_local_datetime",
        "carrier",
        "lane",
        "online_atc",
        "past_atcs",
        "status"
    )
    list_filter = ["sch_local_datetime"]
    readonly_fields=("pk",)

# Register your models here.
admin.site.register(Lane)
admin.site.register(ArrivalFlight, ArrivalDeparture)
admin.site.register(DepartureFlight, ArrivalDeparture)
admin.site.register(AirTrafficController)