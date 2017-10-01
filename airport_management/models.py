from datetime import timedelta
from django.db import models

# Create your models here.
class Lane(models.Model):
    name = models.CharField(max_length=7)

    def __str__(self):
        return self.name

class ArrivalDepartureFlight(models.Model):
    # Non-null-able fields.

    # Flight code.
    flight_code = models.CharField(max_length=10)

    # The other airport that is not this airport.
    airport = models.CharField(max_length=3)

    """
    The day the flight happens, arriving or departing from this airport
    perspective.

    PENDING: This could be made as an enumeration because the value will only
    be strictly for strings of days (Monday to Sunday).
    """
    day = models.CharField(max_length=9)

    # Scheduled arrival or departure time.
    scheduled_datetime = models.DateTimeField()

    # Null-able fields.

    # Flight's organization name.
    carrier = models.CharField(max_length=20, null=True)

    """
    Lane used for arriving or departing. This field has one to many
    relationship to the `Lane` model. The `related_name="%(class)s_lane"` is
    used to prevent `Error: One or more models did not validate:` error.

    PENDING: This field are supposed to have one to one relationship due to
    every lanes can only be used for one flight. I just make this one to many
    """
    lane = models.ForeignKey("Lane", null=True, on_delete=models.CASCADE,
        related_name="%(class)s_lane")

    # Current air traffic controller (ATC).
    online_atcs = models.ManyToManyField("AirTrafficController",
        related_name="%(class)s_online_atc")

    """
    Whether a flight has assigned to ATC and lane during the
    `scheduled_time` or not.
    """
    status = models.NullBooleanField(null=True)

    """
    Real arrival/departure time. If the value of this field is not `None` or
    `null` then this flight is already arrived/departed.

    CAUTION: This field is not currently being used.
    """
    #real_local_time = models.DateTimeField(null=True)

    """
    List of all previous air traffic controllers.

    CAUTION: This field is not currently being used.
    """
    #past_atcs = models.ForeignKey("AirTrafficController", null=True,
    #    on_delete=models.CASCADE, related_name="%(class)s_past_atcs")

    class Meta:
        abstract = True

class ArrivalFlight(ArrivalDepartureFlight):
    def __str__(self):
        return "{} from {} airport, {}".format(
            self.flight_code,
            self.airport,
            self.scheduled_datetime
        )

class DepartureFlight(ArrivalDepartureFlight):
    def __str__(self):
        return "{} to {} airport, {}".format(
            self.flight_code,
            self.airport,
            self.scheduled_datetime
        )


class AirTrafficController(models.Model):
    # Code name for the ATC.
    code = models.CharField(max_length=10, unique=True)

    # The first name and the last name of the ATC.
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    """
    The ideal is that these two fields are combined. But it is impossible to
    refer `ForeignKey` to `ArrivalDeparture` abstract model.

    CAUTION: These fields are not currently being used.
    """
    #past_flights_arrival = models.ForeignKey("ArrivalFlight", null=True,
    #    on_delete=models.CASCADE)
    #past_flights_departure = models.ForeignKey("DepartureFlight", null=True,
    #    on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)