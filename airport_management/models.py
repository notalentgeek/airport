from django.db import models
from django.utils.timezone import localtime

# Create your models here.
class Lane(models.Model):
    name = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class ArrivalDepartureFlight(models.Model):
    ########## Non-null-able fields. ##########
    # The airplane code.
    flight_code = models.CharField(max_length=10)

    # The other airport (not this airport).
    airport = models.CharField(max_length=3)

    """
    The day the operation happens arriving/departing from this airport
    perspective.
    """
    day = models.CharField(max_length=9)

    # Scheduled arrival/departure time.
    sch_local_datetime = models.DateTimeField()

    ########## Null-able fields. ##########
    # The airplane brand name.
    carrier = models.CharField(max_length=20, null=True)

    #Lane used for arriving/departing.
    lane = models.OneToOneField("Lane", null=True, on_delete=models.CASCADE,
        related_name="%(class)s_lane")

    """
    Real arrival/departure time. If the value of this field is not `None` or
    `null` then this flight is already arrived/departed.

    This field is currently not being used.
    """
    #real_local_time = models.DateTimeField(null=True)

    # Current air traffic controller (ATC).
    online_atc = models.ForeignKey("AirTrafficController", null=True,
        on_delete=models.CASCADE, related_name="%(class)s_online_atc")

    # List of all previous air traffic controllers.
    past_atcs = models.ForeignKey("AirTrafficController", null=True,
        on_delete=models.CASCADE, related_name="%(class)s_past_atcs")

    # Whether the flight has proper communications with online ATC.
    proper_atc = models.NullBooleanField(null=True)

    def __str__(self):
        return "{} from {} airport, {}".format(
            self.flight_code,
            self.airport,
            localtime(self.sch_local_datetime)
        )

    class Meta:
        abstract = True

class ArrivalFlight(ArrivalDepartureFlight): pass
class DepartureFlight(ArrivalDepartureFlight): pass

class AirTrafficController(models.Model):
    # Code name for the ATC.
    code = models.CharField(max_length=10, unique=True)

    # The first name and the last name of the ATC.
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    """
    The ideal is that these two fields are combined. But it is impossible to
    refer `ForeignKey` to `ArrivalDeparture` abstract model.
    """
    past_flights_arrival = models.ForeignKey("ArrivalFlight", null=True,
        on_delete=models.CASCADE)
    past_flights_departure = models.ForeignKey("DepartureFlight", null=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)