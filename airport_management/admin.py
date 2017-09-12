from django.contrib import admin
from .models import AirTrafficController, ArrivalFlight, DepartureFlight, Lane

class ArrivalDepartureModel(admin.ModelAdmin):
    list_display = (
        "pk",
        "flight_code",
        "airport",
        "day",
        "scheduled_datetime",
        "carrier",
        "lane",
        "status"
    )
    list_filter = ["scheduled_datetime"]
    readonly_fields=("pk",)

# Register your models here.
admin.site.register(Lane)
admin.site.register(ArrivalFlight, ArrivalDepartureModel)
admin.site.register(DepartureFlight, ArrivalDepartureModel)
admin.site.register(AirTrafficController)