from .models import ArrivalFlight, DepartureFlight
from .src.flight_api_puller import get_public_flight_api
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from datetime import timedelta
from django.db.models import Q
from os import remove
from os.path import dirname, join, normcase, normpath, realpath
from pytz import timezone
from subprocess import call
from sys import argv
import datetime

logger = get_task_logger(__name__)

#@periodic_task(run_every=crontab(minute="*/15"))
#@periodic_task(run_every=timedelta(minutes=10))
#@periodic_task(run_every=timedelta(minutes=2))
#@periodic_task(run_every=timedelta(minutes=5))
#@periodic_task(run_every=timedelta(seconds=1))
#@periodic_task(run_every=timedelta(seconds=5))
@periodic_task(run_every=crontab(minute=0, hour="0"))
def flight_api_pull():
    flights = get_public_flight_api()

    for flight in flights:
        flight_id = flight["id"]
        if flight["direction"] == "A":
            get_input_save(ArrivalFlight, flight)
        elif flight["direction"] == "D":
            get_input_save(DepartureFlight, flight)

    update_all_proper_atc()
    create_backup_fixtures()

"""
Task to periodically marked which flights has properly arrived/departed. The
parameters are to have both ATC and lane set when the flight arrives/departs.
"""
@periodic_task(run_every=timedelta(minutes=1))
def check_this_minute_proper_atc():
    tz = timezone("Europe/Amsterdam")
    now = tz.localize(datetime.datetime.now())
    now_1_min = now + timedelta(minutes=1)

    """
    Arrival and departure time filter based on the time and if "proper" flag
    is already set.
    """
    arrival_filter = ArrivalFlight.objects.filter(proper_atc__isnull=True,
        sch_local_datetime__lt = now_1_min)
    departure_filter = DepartureFlight.objects.filter(proper_atc__isnull=True,
        sch_local_datetime__lt = now_1_min)

    """
    Arrival and departure time filter based on conditions (lane and online ATC
    exist).
    """
    arrival_filter_proper = arrival_filter.filter(Q(lane__isnull=False) &\
        Q(online_atc__isnull=False))
    arrival_filter_not_proper = arrival_filter.filter(Q(lane__isnull=True) |\
        Q(online_atc__isnull=True))
    departure_filter_proper = departure_filter.filter(Q(lane__isnull=False) &\
        Q(online_atc__isnull=False))
    departure_filter_not_proper = departure_filter.filter(Q(lane__isnull=True)\
        | Q(online_atc__isnull=True))

    arrival_filter_proper.update(proper_atc=True)
    arrival_filter_not_proper.update(proper_atc=False)
    departure_filter_proper.update(proper_atc=True)
    departure_filter_not_proper.update(proper_atc=False)

# Create fixtures every time API saved into database.
def create_backup_fixtures():
    # Path to the root of this Django project (not Django application!).
    file_executed_location = dirname(realpath(argv[0]))

    # Path to manage.py
    manage_py = "manage.py"
    manage_py = join(file_executed_location, manage_py)
    manage_py = normpath(normcase(manage_py))

    # Path to airport management fixtures.
    fixtures_directory = "airport_management/fixtures/airport_management"

    # Path to arrival fixtures.
    arrival_fixtures = "arrival_flight.json"
    arrival_fixtures = join(fixtures_directory, arrival_fixtures)
    arrival_fixtures = join(file_executed_location, arrival_fixtures)

    # DPath to departure fixtures.
    departure_fixtures = "departure_flight.json"
    departure_fixtures = join(fixtures_directory, departure_fixtures)
    departure_fixtures = join(file_executed_location, departure_fixtures)

    # Remove arrival fixtures before this program created new ones.
    try:
        remove(arrival_fixtures)
    except FileNotFoundError as error:
        print(error)
    try:
        remove(departure_fixtures)
    except FileNotFoundError as error:
        print(error)

    # Create the fixtures back.
    call(["python3 -B {} dumpdata airport_management.ArrivalFlight --indent 4 >\
        {}".format(manage_py, arrival_fixtures)], shell=True)
    call(["python3 -B {} dumpdata airport_management.DepartureFlight --indent 4\
        > {}".format(manage_py, departure_fixtures)], shell=True)

"""
Function to get an element from the primary key (`pk`), but if there is none
create a new instance of its model.
"""
def get_or_create(model, pk_value):
    get_model = model.objects.filter(pk=pk_value)
    if get_model.exists():
        """
        Only get the first element. Although filtering using `pk` will always
        return an element.
        """
        return get_model[0]
    else:
        # Assign newly created model.
        return model()

# Function to get the flight document, input or update new value, then save it.
def get_input_save(arrivaldeparture_flight, flight):
    model = get_or_create(arrivaldeparture_flight, flight["id"])
    model = input_to_model_for_arrivaldeparture_flight(model,
        flight)
    model.save()
    return model

def input_to_model_for_arrivaldeparture_flight(arrivaldeparture_flight,
    flight):
    arrivaldeparture_flight.id = flight["id"]
    arrivaldeparture_flight.direction = flight["direction"]
    arrivaldeparture_flight.flight_code = flight["flight_code"]
    arrivaldeparture_flight.airport = flight["airport"]
    arrivaldeparture_flight.sch_local_datetime =\
        flight["sch_local_datetime"]
    arrivaldeparture_flight.day = flight["day"]

    if "carrier" in flight:
        arrivaldeparture_flight.carrier = flight["carrier"]

    return arrivaldeparture_flight

# Function to update all flights that were not maintained by ATC.
def update_all_proper_atc():
    tz = timezone("Europe/Amsterdam")
    now = tz.localize(datetime.datetime.now())

    # Get all past flights which has `proper_atc` blank.
    not_proper_arrival = ArrivalFlight.objects.filter(
        sch_local_datetime__lt=now,
        proper_atc__isnull=True
    )
    not_proper_departure = DepartureFlight.objects.filter(
        sch_local_datetime__lt=now,
        proper_atc__isnull=True
    )

    # Set all past flights with no proper ATC to false.
    not_proper_arrival.update(proper_atc=False)
    not_proper_departure.update(proper_atc=False)