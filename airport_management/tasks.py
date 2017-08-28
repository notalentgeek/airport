from .models import ArrivalFlight, DepartureFlight
from .src.flight_api_puller import get_public_flight_api
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from datetime import datetime
from datetime import timedelta

logger = get_task_logger(__name__)

#@periodic_task(run_every=timedelta(seconds=1))
@periodic_task(run_every=timedelta(seconds=5))
#@periodic_task(run_every=crontab(minute="*/15"))
def flight_api_pull():
    flights = get_public_flight_api()

    for flight in flights:
        flight_id = flight["id"]
        if flight["direction"] == "A":
            get_input_save(ArrivalFlight, flight)
        elif flight["direction"] == "D":
            get_input_save(DepartureFlight, flight)

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
    arrivaldeparture_flight.carrier = flight["carrier"]
    arrivaldeparture_flight.flight_code = flight["flight_code"]
    arrivaldeparture_flight.airport = flight["airport"]
    arrivaldeparture_flight.sch_local_datetime =\
        flight["sch_local_datetime"]
    arrivaldeparture_flight.day = flight["day"]

    return arrivaldeparture_flight