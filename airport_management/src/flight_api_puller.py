from .date_and_time import get_day_from_datetime
from datetime import datetime
import requests, sys

def get_public_flight_api():
    """
    API application id and API application key. The API used is the Schipol
    airport API, https://developer.schiphol.nl/.
    """
    APP_ID = "9aaba5a2"
    APP_KEY = "34a904ec4b046880b5a3ee94f18be45a"
    CREDENTIALS = { "app_id": APP_ID, "app_key": APP_KEY }

    # Main GET URL.
    URL = "https://api.schiphol.nl/public-flights/flights"

    HEADERS = { "resourceversion": "v3" }

    """
    Get the API feed for flight schedule in Schipol. If there is no connection
    then `return None`.
    """
    try:
        response = requests.request("GET", URL, headers=HEADERS,
            params=CREDENTIALS)
    except requests.exceptions.ConnectionError as error:
        print(error)
        return None

    return_dictionary_list = []

    if response.status_code == 200:
        flights = response.json()
        for flight in flights["flights"]:
            return_dictionary = {}

            # All model for both arrival and departure.
            json_id = flight["id"]
            arrival_or_departure = flight["flightDirection"]
            carrier = flight ["prefixICAO"]
            flight_code = flight["flightName"]
            sch_departure_date = flight["scheduleDate"]
            sch_departure_time = flight["scheduleTime"]
            sch_departure_date_time = "{}T{}".format(sch_departure_date,
                sch_departure_time)
            sch_departure_date_time_datetime = datetime.strptime(
                sch_departure_date_time,
                "%Y-%m-%dT%H:%M:%S"
            )
            day = get_day_from_datetime(sch_departure_date_time_datetime)
            airport = flight["route"]["destinations"][0]

            return_dictionary["json_id"] = json_id
            return_dictionary["arrival_or_departure"] = arrival_or_departure
            return_dictionary["carrier"] = carrier
            return_dictionary["flight_code"] = flight_code
            return_dictionary["airport"] = airport
            return_dictionary["sch_departure_date_time_datetime"] =\
                sch_departure_date_time_datetime
            return_dictionary["day"] = day

            if arrival_or_departure == "A":
                # Arrival specific fields.
                expected_arrival_local_date_time = flight["estimatedLandingTime"]
                real_arrival_local_date_time = flight["actualLandingTime"]
                arrived = False

                return_dictionary["expected_arrival_local_date_time"] =\
                    expected_arrival_local_date_time

                if (real_arrival_local_date_time != None):
                    arrived = True
                    return_dictionary["real_arrival_local_date_time"] =\
                        real_arrival_local_date_time

                return_dictionary["arrived"] = arrived

            return_dictionary_list.append(return_dictionary)

        return return_dictionary_list
    else:
        print("something went wrong, http response code {}\n{}".format(
            response.status_code, response.text))
        return None