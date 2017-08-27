from .models import Arrival, Departure
from .src.flight_api_puller import get_public_flight_api
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from datetime import datetime
from datetime import timedelta

logger = get_task_logger(__name__)

@periodic_task(run_every=timedelta(seconds=5))
def flight_api_pull():
    """
    flights = get_public_flight_api()

    for flight in flights:
        if flight["arrival_or_departure"] == "A":
            if flight["arrived"]:
                if Arrival.objects.filter(pk=flight["json_id"]).exists():
                    Arrival.objects.filter(pk=flight["json_id"]).update(
                        id=flight["json_id"],
                        flight_code=flight["flight_code"],
                        carrier=flight["carrier"],
                        day=flight["day"],
                        sch_departure_date=flight["sch_departure_date_time_datetime"],
                        airport=flight["airport"],
                        expected_arrival_local_date=
                            flight["expected_arrival_local_date_time"],
                        real_arrival_local_date=flight["real_arrival_local_date_time"],
                        arrived=True
                    )
                else:
                    Arrival.objects.create(
                        id=flight["json_id"],
                        flight_code=flight["flight_code"],
                        carrier=flight["carrier"],
                        day=flight["day"],
                        sch_departure_date=flight["sch_departure_date_time_datetime"],
                        airport=flight["airport"],
                        expected_arrival_local_date=
                            flight["expected_arrival_local_date_time"],
                        real_arrival_local_date=flight["real_arrival_local_date_time"],
                        arrived=True
                    )
            else:
                if Arrival.objects.filter(pk=flight["json_id"]).exists():
                    Arrival.objects.filter(pk=flight["json_id"]).update(
                        id=flight["json_id"],
                        flight_code=flight["flight_code"],
                        carrier=flight["carrier"],
                        day=flight["day"],
                        sch_departure_date=flight["sch_departure_date_time_datetime"],
                        airport=flight["airport"],
                        expected_arrival_local_date=
                            flight["expected_arrival_local_date_time"],
                        arrived=False
                    )
                else:
                    Arrival.objects.create(
                        id=flight["json_id"],
                        flight_code=flight["flight_code"],
                        carrier=flight["carrier"],
                        day=flight["day"],
                        sch_departure_date=flight["sch_departure_date_time_datetime"],
                        airport=flight["airport"],
                        expected_arrival_local_date=
                            flight["expected_arrival_local_date_time"],
                        arrived=False
                    )
        elif flight["arrival_or_departure"] == "D":
            if Departure.objects.filter(pk=flight["json_id"]).exists():
                Departure.objects.filter(pk=flight["json_id"]).update(
                    id=flight["json_id"],
                    flight_code=flight["flight_code"],
                    carrier=flight["carrier"],
                    day=flight["day"],
                    sch_departure_date=flight["sch_departure_date_time_datetime"],
                    airport=flight["airport"]
                )
            else:
                Departure.objects.create(
                    id=flight["json_id"],
                    flight_code=flight["flight_code"],
                    carrier=flight["carrier"],
                    day=flight["day"],
                    sch_departure_date=flight["sch_departure_date_time_datetime"],
                    airport=flight["airport"]
                )

    """

    # Debug to terminal console.
    #logger.info(flights)
    # Debug to static file.
    #log = open("/home/mikael/Downloads/airport/airport_management/log.txt", "a")
    #print(flights, file=log)
    #log.close()
    logger.info("hello world")