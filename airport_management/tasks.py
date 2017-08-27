from .models import Arrival, Departure
from .src.flight_api_puller import get_public_flight_api
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from datetime import datetime
from datetime import timedelta

logger = get_task_logger(__name__)

#@periodic_task(run_every=timedelta(seconds=1))
#@periodic_task(run_every=timedelta(seconds=5))
@periodic_task(run_every=crontab(minute="*/15"))
def flight_api_pull():
    flights = get_public_flight_api()

    for flight in flights:
        if flight["direction"] == "A":
            arrival = get_or_create(Arrival, flight["id"])
            arrival = input_to_database_for_arrivaldeparture(arrival, flight)

            arrival.sch_arrival_local_datetime =\
                flight["sch_arrival_local_datetime"]

            if "real_arrival_local_datetime" in flight:
                arrival.real_arrival_local_datetime =\
                    flight["real_arrival_local_datetime"]

            arrival.save()
        elif flight["direction"] == "D":
            departure = get_or_create(Departure, flight["id"])
            departure = input_to_database_for_arrivaldeparture(departure,
                flight)
            departure.save()


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

def input_to_database_for_arrivaldeparture(arrivaldeparture, flight):
    arrivaldeparture.id = flight["id"]
    arrivaldeparture.direction = flight["direction"]
    arrivaldeparture.carrier = flight["carrier"]
    arrivaldeparture.flight_code = flight["flight_code"]
    arrivaldeparture.sch_departure_datetime = flight["sch_departure_datetime"]
    arrivaldeparture.day = flight["day"]
    arrivaldeparture.airport = flight["airport"]

    return arrivaldeparture