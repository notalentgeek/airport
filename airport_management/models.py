from django.db import models

# Create your models here.
class ArrivalDeparture(models.Model):
    ########## Non-null-able fields. ##########
    # The airplane brand name.
    carrier = models.CharField(max_length=20)

    # The airplane code.
    flight_code = models.CharField(max_length=10)

    # Scheduled departure date and time.
    sch_departure_datetime = models.DateTimeField(blank=True)

    """
    The day the operation happens arriving/departing from this airport
    perspective.
    """
    day = models.CharField(max_length=9)

    # The other airport (not this airport).
    airport = models.CharField(max_length=3)

    ########## Null-able fields. ##########
    # Current air traffic controller (ATC).
    online_atc = models.OneToOneField("AirTrafficController", blank=True,
        null=True, on_delete=models.CASCADE,
        related_name="%(class)s_online_atc")

    # List of all previous air traffic controllers.
    past_atcs = models.ForeignKey("AirTrafficController", blank=True,
        null=True, on_delete=models.CASCADE, related_name="%(class)s_past_atcs")

    # Whether the flight has proper communications with online ATC.
    proper_atc = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Arrival(ArrivalDeparture):
    # This airport's flight arrival date and time.
    sch_arrival_local_datetime = models.DateTimeField(blank=True)

    """
    The flight's date and time real arrival date and time (with delay, ...).
    If the `real_arrival_local_datetime` not null or None then the flight is
    arrived.
    """
    real_arrival_local_datetime = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{} from {}, {}".format(
            self.flight_code,
            self.airport,
            self.sch_arrival_local_datetime
        )

class Departure(ArrivalDeparture):
    def __str__(self):
        return "{} to {}, {}".format(
            self.flight_code,
            self.airport,
            self.sch_departure_datetime
        )

class AirTrafficController(models.Model):
    # Code name for the ATC.
    code = models.CharField(max_length=10)

    # The first name and the last name of the ATC.
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    """
    The ideal is that these two fields are combined. But it is impossible to
    refer `ForeignKey` to `ArrivalDeparture` abstract model.
    """
    past_flights_arrival = models.ForeignKey("Arrival", blank=True,
        null=True, on_delete=models.CASCADE)
    past_flights_departure = models.ForeignKey("Departure", blank=True,
        null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(first_name, last_name)