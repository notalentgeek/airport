from .models import ArrivalFlight, DepartureFlight
from .src.flight_api_puller import get_public_flight_api
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from os import remove
from os.path import dirname, join, normcase, normpath, realpath
from subprocess import call
from sys import argv

logger = get_task_logger(__name__)

#@periodic_task(run_every=crontab(minute="*/15"))
@periodic_task(run_every=crontab(minute=0, hour="0"))
#@periodic_task(run_every=timedelta(minutes=10))
#@periodic_task(run_every=timedelta(minutes=2))
#@periodic_task(run_every=timedelta(minutes=5))
#@periodic_task(run_every=timedelta(seconds=1))
#@periodic_task(run_every=timedelta(seconds=5))
def flight_api_pull():
    flights = get_public_flight_api()

    for flight in flights:
        flight_id = flight["id"]
        if flight["direction"] == "A":
            get_input_save(ArrivalFlight, flight)
        elif flight["direction"] == "D":
            get_input_save(DepartureFlight, flight)

    create_backup_fixtures()

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