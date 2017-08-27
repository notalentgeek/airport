from datetime import datetime
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

            if flight["flightDirection"] == "A":

                return_dictionary["sch_arrival_local_datetime"] =\
                    flight["estimatedLandingTime"]

                real_arrival_local_datetime = flight["actualLandingTime"]
                if real_arrival_local_datetime !=  "None" or\
                    real_arrival_local_datetime !=  None:
                    return_dictionary["real_arrival_local_datetime"] =\
                        real_arrival_local_datetime

            return_dictionary_list.append(return_dictionary)


        return return_dictionary_list
    else:
        print("something went wrong, http response code {}\n{}".format(
            response.status_code, response.text))
        return None

def make_dictionary_for_arrivaldeparture(dictionary, flight):
    dictionary["id"] = flight["id"]
    dictionary["direction"] = flight["flightDirection"]
    dictionary["carrier"] = flight["prefixICAO"]
    dictionary["flight_code"] = flight["mainFlight"]

    sch_departure_date = flight["scheduleDate"]
    sch_departure_time = flight["scheduleTime"]

    #print("="*50)
    #print("{}: {}".format("sch_departure_date", sch_departure_date))
    #print("{}: {}".format("sch_departure_time", sch_departure_time))

    sch_departue_timezone = timezone("Europe/Amsterdam")
    sch_departure_datetime = "{}T{}".format(sch_departure_date,
        sch_departure_time)
    dictionary["sch_departure_datetime"] = sch_departue_timezone.localize(
        datetime.strptime(
            sch_departure_datetime,
            "%Y-%m-%dT%H:%M:%S"
        )
    )

    #print("{}: {}".format(dictionary["sch_departure_datetime"],
    #    dictionary["sch_departure_datetime"]))
    #print("="*50)

    dictionary["day"] = get_day_from_datetime(
        dictionary["sch_departure_datetime"])

    dictionary["airport"] =\
        flight["route"]["destinations"][0]

    return dictionary

if __name__ == "__main__":
    get_public_flight_api()