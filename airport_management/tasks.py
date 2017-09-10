from .models import ArrivalFlight, DepartureFlight
from .src.flight_api_puller import get_public_flight_api
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from datetime import timedelta
from django.db.models import Q
from enum import Enum
from os import remove
from os.path import dirname, join, normcase, normpath, realpath
from pytz import timezone
from subprocess import call
from sys import argv
import datetime

class AOD(Enum):
    ARRIVAL = "A"
    DEPARTURE = "D"

# PENDING: Get the timezone determined automatically.
TIMEZONE = timezone("Europe/Amsterdam")

logger = get_task_logger(__name__)

"""
Periodically pull data from the API into the database, update the flight
statuses, and create backup fixtures.
"""
#@periodic_task(run_every=crontab(minute="*/15"))
#@periodic_task(run_every=timedelta(minutes=10))
#@periodic_task(run_every=timedelta(minutes=2))
#@periodic_task(run_every=timedelta(minutes=5))
#@periodic_task(run_every=timedelta(seconds=1))
#@periodic_task(run_every=timedelta(seconds=5))
@periodic_task(run_every=crontab(minute=0, hour="0"))
def flight_api_pull():
    flights = get_public_flight_api()

    # Iterate through all available flights.
    for flight in flights:
        if flight["direction"] == AOD.ARRIVAL:
            get_input_save(ArrivalFlight, flight)
        elif flight["direction"] == AOD.DEPARTURE:
            get_input_save(DepartureFlight, flight)

    # Update all flight statuses.
    update_all_flight_statuses()

    # Create backup from arrival table and departure table into fixtures.
    create_backup_arrivaldeparture_flight_fixtures()

"""
Task to periodically marked which flight has properly arrived or departed. The
parameters are to have both ATC and lane set when the corresponding flight
arrives or departed.
"""
@periodic_task(run_every=timedelta(minutes=1))
def check_flight_statuses():
    # Get the date and time for current operation.
    now = TIMEZONE.localize(datetime.datetime.now())

    # Get the date and time for current operation with additional one minute.
    now_1_min = now + timedelta(minutes=1)

    """
    Get all flights that from this minutes and smaller then another one
    minute.
    """
    arrival_flights = return_all_objects_in_this_minute(ArrivalFlight, now,
        now_1_min, { "status__isnull": True })
    departure_flights = return_all_objects_in_this_minute(DepartureFlight, now,
        now_1_min, { "status__isnull": True })

    flight_update_status_based_on_atc_and_lane(arrival_flights)
    flight_update_status_based_on_atc_and_lane(departure_flights)

"""
Function to update flight status based on the availability of `lane` and
`atc_online`.

PENDING: I think this part could be improved, because here, the `update()`
function runs twice.
"""
def flight_update_status_based_on_atc_and_lane(flight_objects):
    flight_objects.filter(Q(lane__isnull=True) | Q(online_atc__isnull=True))
        .update(status=False)
    flight_objects.filter(lane__isnull=False, online_atc__isnull=False)
        .update(status=True)

# Function to get flight objects, create new or update the value, then save it.
def get_input_save(model, flight_dict):
    flight_object = get_or_create_object(model, flight_dict["id"])
    flight_object = set_model_for_arrivaldeparture_flight(flight_object,
        flight_dict)
    flight_object.save()

    return flight_object

"""
Function to get an element from the primary key (`pk`), but if there is none
create a new instance of its model.
"""
def get_or_create_object(model, pk_value):
    object_ = model.objects.filter(pk=pk_value)
    if object_.exists():
        """
        Only get the first element. Although filtering using `pk` will always
        return an element.
        """
        return object_[0]
    else:
        # Assign newly created model.
        return model()

"""
Function to return all objects in a table with `datetime` parameter in this
minute.
"""
def return_all_objects_in_this_minute(model, now, now_1_min, additional_dict):
    return model.objects.filter(
        scheduled_datetime__gte=now,
        scheduled_datetime__lt=now_1_min,
        **{ additional_dict }
    )

# Set the `ArrivalDepartureFlight` document with values.
def set_model_for_arrivaldeparture_flight(flight_object, flight_dict):
    flight_object.airport = flight_dict["airport"]
    flight_object.day = flight_dict["day"]
    flight_object.direction = flight_dict["direction"]
    flight_object.flight_code = flight_dict["flight_code"]
    flight_object.id = flight_dict["id"]
    flight_object.scheduled_datetime = flight_dict["scheduled_datetime"]

    if "carrier" in flight_dict:
        flight_object.carrier = flight_dict["carrier"]

    return flight_object

# Update all flight statuses.
def update_all_flight_statuses():
    def update_all_flight_statuses_(model):
        model.objects.filter(
            scheduled_datetime__lt=now,
            status__isnull=True
       ).update(status=False)

    # Get the date and time for current operation.
    now = TIMEZONE.localize(datetime.datetime.now())

    # Get all flights which has no status, then update it.
    update_all_flight_statuses_(ArrivalFlight)
    update_all_flight_statuses_(DepartureFlight)