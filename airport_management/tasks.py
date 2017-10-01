"""
Celery task file.

PENDING: A lot of closures should be made here.
"""

from .models import ArrivalFlight, DepartureFlight
from .src.consts import API_KEY, PATH, STRING
from .src.flight_api_puller import get_public_flight_api
from celery.decorators import periodic_task
from celery.five import monotonic
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from collections import namedtuple
from contextlib import contextmanager
from datetime import timedelta
from django.core.cache import cache
from django.db.models import Q
from hashlib import md5
from os import remove
from os.path import dirname, join, normcase, normpath, realpath
from pytz import timezone, utc
from subprocess import call
from sys import argv
import datetime

LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes

logger = get_task_logger(__name__) # Celery inside operation.

""" Prevent task to overlap to each other. """
@contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = monotonic() + LOCK_EXPIRE - 3

    """ cache.add fails if the key already exists. """
    status = cache.add(lock_id, oid, LOCK_EXPIRE)

    try:
        yield status
    finally:
        """
        memcache delete is very slow, but we have to use it to take
        advantage of using add() for atomic locking
        """
        if monotonic() < timeout_at:
            """
            Do not release the lock if we exceeded the timeout to lessen the
            chance of releasing an expired lock owned by someone else.
            """
            cache.delete(lock_id)

"""
Celery task to periodically pull API in the midnight. Use this periodic
function to debug only, otherwise use the `flight_api_pull_()` for production.

Un-commment the decorator if you just want to pull the flights API.
"""
#@periodic_task(run_every=timedelta(minutes=1))
def flight_api_pull():
    """
    The cache key consists of the task name and the MD5 digest of the feed
    URL.
    """
    lock_id = "flight-api-pull-lock-id"
    lock_oid = "flight-api-pull-lock-oid"
    with memcache_lock(lock_id, lock_oid) as acquired:
        if acquired:
            return flight_api_pull_()
    logger.debug("task is already ran")

""" Comment the decorator if you just want to pull the flights API. """
@periodic_task(run_every=crontab(minute=0, hour=0))
def flight_api_pull_():
    flights = get_public_flight_api()

    for flight in flights:
        if flight[API_KEY.DIRECTION] == API_KEY.ARRIVAL:
            get_input_then_save(ArrivalFlight, flight)
        if flight[API_KEY.DIRECTION] == API_KEY.DEPARTURE:
            get_input_then_save(DepartureFlight, flight)

    # Update all flights status.
    update_all_flights_status()

    # Create backup fixtures.
    create_backup_fixtures()

"""
Task to periodically marked which flights has properly arrived/departed. The
parameters are to have both ATCs and a lane set when the actual arriving/
departing time passed.

Comment the decorator if you just want to pull flights API.
"""
@periodic_task(run_every=timedelta(minutes=1))
def check_this_minute_flights_status():
    tz = timezone(STRING.TIMEZONE)
    #now = datetime.datetime.now()
    now = datetime.datetime.now(utc)
    now_plus_1_min = now + timedelta(minutes=1)

    """ PENDING: Please make some closures for this function. """

    """
    Arrival and departure time filter based on the time and if "proper" flag
    is already set.
    """
    arrival_filter = ArrivalFlight.objects.filter(status__isnull=True)\
        .filter(scheduled_datetime__lte=now_plus_1_min)
    departure_filter = DepartureFlight.objects.filter(status__isnull=True)\
        .filter(scheduled_datetime__lte=now_plus_1_min)

    """
    Arrival and departure time filter based on conditions (lane and online
    ATCs exist).
    """
    arrival_filter_not_proper = arrival_filter.filter(
        Q(lane__isnull=True) |
        Q(online_atcs__isnull=True)
    )
    arrival_filter_proper = arrival_filter.filter(
        Q(lane__isnull=False) &
        Q(online_atcs__isnull=False)
    )
    departure_filter_not_proper = departure_filter.filter(
        Q(lane__isnull=True) |
        Q(online_atcs__isnull=True)
    )
    departure_filter_proper = departure_filter.filter(
        Q(lane__isnull=False) &
        Q(online_atcs__isnull=False)
    )

    arrival_filter_not_proper.update(status=False)
    arrival_filter_proper.update(status=True)
    departure_filter_not_proper.update(status=False)
    departure_filter_proper.update(status=True)

"""
Backup to fixtures every 10 minutes.

Comment the decorator if you only want to pull the flight API.
"""
periodic_task(run_every=timedelta(minutes=10))
def create_backup_fixtures_():
    create_backup_fixtures()

def normcase_normpath(path):
    return normcase(normpath(path))

""" Create/update fixtures everytime API saved into database. """
def create_backup_fixtures():
    """ Path to the root of this Django project (not this Django application).
    This can be done because the location of manage.py that is always in the
    root of a Django project. """
    file_executed_location = dirname(realpath(argv[0]))

    """ Path to manage.py. """
    manage_py_path = join(file_executed_location, STRING.MANAGE_PY)
    manage_py_path = normcase_normpath(manage_py_path)

    """ Path to manage.py. """
    fixtures_directory = normcase_normpath(PATH.APPLICATION_FIXTURES)

    """ Path to arrival flight fixture. """
    arrival_fixture_path = join(fixtures_directory,
        STRING.ARRIVAL_FLIGHT_JSON_FIXTURE)
    arrival_fixture_path = join(file_executed_location,
        arrival_fixture_path)

    """ Path to departure flight fixture. """
    departure_fixture_path = join(fixtures_directory,
        STRING.DEPARTURE_FLIGHT_JSON_FIXTURE)
    departure_fixture_path = join(file_executed_location,
        departure_fixture_path)

    """ Path to Air Traffic Controller fixture. """
    atc_fixture_path = join(fixtures_directory,STRING.ATC_JSON_FIXTURE)
    atc_fixture_path = join(file_executed_location, atc_fixture_path)

    """ Create the fixtures back from database. """
    call(["python3 -B {} dumpdata airport_management.ArrivalFlight --indent \
        4 > {}".format(manage_py_path, arrival_fixture_path)], shell=True)
    call(["python3 -B {} dumpdata airport_management.DepartureFlight \
        --indent 4 > {}".format(manage_py_path, departure_fixture_path)],
        shell=True)
    call(["python3 -B {} dumpdata airport_management.AirTrafficController \
        --indent 4 > {}".format(manage_py_path, atc_fixture_path)],
        shell=True)

""" Function to get an element from the primary key (`pk`), but if there is
none, create a new instance of its modal.
"""
def get_or_create(model, pk_value):
    get_model = model.objects.filter(pk=pk_value)

    if get_model.exists():
        """
        Only get the first element. Although, filtering using `pk` will always
        return an element, because `px` is an unique ID field.
        """
        return get_model[0]
    else:
        """
        If there is no document exists return  a newly created model.
        """
        return model()

"""
Function to get the flight document, input or update new value, then save it.
"""
def get_input_then_save(arrivaldeparture_flight, flight_data):
    model = get_or_create(arrivaldeparture_flight, flight_data[API_KEY.ID])
    model = input_to_model_for_arrivaldeparture_flight(model, flight_data)
    model.save()
    return model

def input_to_model_for_arrivaldeparture_flight(arrivaldeparture_flight,
    flight_data):
    arrivaldeparture_flight.id = flight_data["id"]
    arrivaldeparture_flight.direction = flight_data["direction"]
    arrivaldeparture_flight.flight_code = flight_data["flight_code"]
    arrivaldeparture_flight.airport = flight_data["airport"]
    arrivaldeparture_flight.scheduled_datetime =\
        flight_data["scheduled_datetime"]
    arrivaldeparture_flight.day = flight_data["day"]

    """ I found that not every document has `"carrier"` filled. """
    if "carrier" in flight_data:
        arrivaldeparture_flight.carrier = flight_data["carrier"]

    return arrivaldeparture_flight

def update_all_flights_status():
    tz = timezone(STRING.TIMEZONE)
    #now = datetime.datetime.now()
    now = datetime.datetime.now(utc)

    """ Get all past flight which has blank `status`. """
    not_proper_arrival = ArrivalFlight.objects.filter(
        scheduled_datetime__lt=now,
        status__isnull=True
    )
    not_proper_departure = DepartureFlight.objects.filter(
        scheduled_datetime__lt=now,
        status__isnull=True
    )

    """ Set all flights without status set to `False`. """
    not_proper_arrival.update(status=False)
    not_proper_departure.update(status=False)