from datetime import datetime, timedelta
from pytz import timezone
import requests, sys

if __name__ == "__main__":
    from date_and_time import get_day_from_datetime
else:
    from .date_and_time import get_day_from_datetime

# Function to call Schipol flight API. This API comes in with pagination.
def get_public_flight_api():
    """
    API application id and API application key. The API used is the Schipol
    airport API, https://developer.schiphol.nl/.
    """
    APP_ID = "a4670f09"
    APP_KEY = "27d16d1e9e8962b6abc7dd5a9ec6bef2"
    CREDENTIALS = { "app_id": APP_ID, "app_key": APP_KEY }

    # Initial URL.
    INITIAL_URL = "https://api.schiphol.nl/public-flights/flights"

    # Initial headers.
    INITIAL_HEADERS = { "resourceversion": "v3" }

    # Main list that will hold all dictionary of today's flight.
    flight_raws = []
    flight_raws = get_next_api_pagination(INITIAL_URL, INITIAL_HEADERS,
        "flights", flight_raws, params=CREDENTIALS)

    flights = []
    for flight_raw in flight_raws:
        flights.append(make_dictionary_for_arrivaldeparture(flight_raw,
            altered_hours=0))

    return flights

"""
Function to get the API from the next pagination. The `elements` is a list
to dump each data from each paginations. At any case for both failure and
success return back the `elements`.
"""
def get_next_api_pagination(url, headers, key, elements, params={}):
    try:
        # Get the response.
        response = requests.request("GET", url, headers=headers, params=params)

        # Check for proper response code.
        if response.status_code == 200:
            # Dump the current returned dictionary into the `elements`.
            current_elements = response.json()[key]
            elements.extend(current_elements)

            """
            All links returned with link relation. Link relation (`rel`) can
            be "next", "previous", "first", "last".
            """
            return_links = [link_pagination.split("; ") for link_pagination in\
                response.headers["Link"].replace("<", "").replace(">", "")\
                .split(", ")]

            for return_link in return_links:
                # The the link relation.
                rel = return_link[1].replace("rel=", "").replace("\"", "")

                """
                If the currently examined link is the next URl from the `url`
                then proceed this function again.
                """
                if rel == "next":
                    get_next_api_pagination(return_link[0], headers, key,
                        elements)

        return elements
    except requests.exceptions.ConnectionError as error:
        print(error)
        return elements

# This function is used to adjust the dictionary with my database models.
def make_dictionary_for_arrivaldeparture(flight, altered_hours=5):
    dictionary = {}
    dictionary["id"] = flight["id"]
    dictionary["direction"] = flight["flightDirection"]
    dictionary["flight_code"] = flight["mainFlight"]
    dictionary["airport"] = flight["route"]["destinations"][0]

    sch_local_date = flight["scheduleDate"]
    sch_local_time = flight["scheduleTime"]

    sch_local_tz = timezone("Europe/Amsterdam")
    sch_local_datetime = "{}T{}".format(sch_local_date,
        sch_local_time)
    sch_local_datetime_original = sch_local_tz.localize(
        datetime.strptime(
            sch_local_datetime,
            "%Y-%m-%dT%H:%M:%S"
        )
    )

    """
    The API data pulled from the Schipol API is too late. When the API taken
    the corresponding flight is already arrived/departed. Hence, to simulate the
    airport management "game" I put additional `altered_hours` into the original
    data taken from the Schipol API.
    """
    sch_local_datetime_altered = sch_local_datetime_original +\
        timedelta(hours=altered_hours)
    dictionary["sch_local_datetime"] = sch_local_datetime_altered

    dictionary["day"] = get_day_from_datetime(
        dictionary["sch_local_datetime"])

    carrier = flight["prefixICAO"]
    if carrier != "None" or carrier != None:
        dictionary["carrier"] = flight["prefixICAO"]

    return dictionary

if __name__ == "__main__":
    print(get_public_flight_api())