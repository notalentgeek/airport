from datetime import datetime, timedelta
from pytz import timezone
import requests, sys

if __name__ == "__main__":
    from date_and_time import get_day_from_datetime
else:
    from .date_and_time import get_day_from_datetime

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


    if response.status_code == 200:
        return_dictionary_list = []
        flights = response.json()

        for flight in flights["flights"]:
            return_dictionary = {};
            return_dictionary = make_dictionary_for_arrivaldeparture(
                return_dictionary,
                flight
            )

            return_dictionary_list.append(return_dictionary)

        return return_dictionary_list
    else:
        print("something went wrong, http response code {}\n{}".format(
            response.status_code, response.text))
        return None

def make_dictionary_for_arrivaldeparture(dictionary, flight, altered_hours=5):
    dictionary["id"] = flight["id"]
    dictionary["direction"] = flight["flightDirection"]
    dictionary["carrier"] = flight["prefixICAO"]
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

    print("="*50)
    print("{} - {}".format(sch_local_datetime_original,
        sch_local_datetime_altered))

    dictionary["sch_local_datetime"] = sch_local_datetime_altered

    dictionary["day"] = get_day_from_datetime(
        dictionary["sch_local_datetime"])

    return dictionary

if __name__ == "__main__":
    print(get_public_flight_api())