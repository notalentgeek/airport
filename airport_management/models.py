from django.db import models

# Create your models here.
class ArrivalDeparture(models.Model):
    flight_code = models.CharField(max_length=10)
    carrier = models.CharField(max_length=20)
    origin_airport = models.CharField(max_length=3)
    destined_airport = models.CharField(max_length=3)
    expected_arrival_local_time = models.DateTimeField()
    online_atc = models.OneToOneField("AirTrafficController", blank=True,
        on_delete=models.CASCADE, related_name="%(class)s_online_atc")
    past_atcs = models.ForeignKey("AirTrafficController", blank=True,
        on_delete=models.CASCADE, related_name="%(class)s_past_atcs")

    class Meta:
        abstract = True

class Arrival(ArrivalDeparture):
    real_departure_local_time = models.DateTimeField()
    real_arrival_local_time = models.DateTimeField(blank=True)
    arrived = models.BooleanField(default=False)

    def __str__(self):
        return "{} from {} to {}, {}".format(
            self.flight_code,
            self.origin_airport,
            self.destined_airport,
            self.expected_arrival_local_time
        )

class Departure(ArrivalDeparture):
    expected_departure_local_time = models.DateTimeField()
    real_departure_local_time = models.DateTimeField(blank=True)
    departed = models.BooleanField(default=False)

    def __str__(self):
        return "{} from {} to {}, {}".format(
            self.flight_code,
            self.origin_airport,
            self.destined_airport,
            self.expected_departure_local_time
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
        on_delete=models.CASCADE)
    past_flights_departure = models.ForeignKey("Departure", blank=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(first_name, last_name)