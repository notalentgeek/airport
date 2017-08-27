from django.db import models

# Create your models here.
class ArrivalDeparture(models.Model):
    carrier = models.CharField(max_length=20)
    flight_code = models.CharField(max_length=10)
    sch_departure_date = models.DateTimeField(blank=True)
    day = models.CharField(max_length=9)
    airport = models.CharField(max_length=3)
    online_atc = models.OneToOneField("AirTrafficController", blank=True,
        null=True, on_delete=models.CASCADE, related_name="%(class)s_online_atc")
    past_atcs = models.ForeignKey("AirTrafficController", blank=True,
        null=True, on_delete=models.CASCADE, related_name="%(class)s_past_atcs")
    proper_atc = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Arrival(ArrivalDeparture):
    expected_arrival_local_date = models.DateTimeField(blank=True)
    real_arrival_local_date = models.DateTimeField(blank=True, null=True)
    arrived = models.BooleanField(default=False)

    def __str__(self):
        return "{} from {} to {}, {}".format(
            self.flight_code,
            self.origin_airport,
            self.destined_airport,
            self.expected_arrival_local_date
        )

class Departure(ArrivalDeparture):
    def __str__(self):
        return "{} from {} to {}, {}".format(
            self.flight_code,
            self.origin_airport,
            self.destined_airport
        )

class AirTrafficController(models.Model):
    code = models.CharField(max_length=10)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    busy = models.BooleanField(default=False)

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