""" Specific functions for this Airport Management application. """

from .consts import DOM_CLASS, KEY, STRING
from django.core.paginator import Paginator

""" A function to create pagination for a model. """
def create_pagination_return_page_and_number_of_pages(
    model,          # Model table of which will be paginated.
    order_field,    # Column of which pagination will be sorted into (to
                    # prevent warning a table needs to be sorted).
    amount,         # The amount of objects per pagination.
    returned_page=1 # All objects in pagination page (after being splitted).
):
    paginator = Paginator(model.objects.all().order_by(order_field), amount)
    dictionary = {}
    dictionary[KEY.NUMBER_OF_PAGES] = paginator.num_pages
    dictionary[KEY.OBJECTS] = paginator.page(returned_page).object_list

    return dictionary

""" Function to generate flight management panel DOM. """
def generate_flight_management_panel_dom_parameters(arrivaldeparture_flight):
    flight_management_panel_dom_ = { KEY.CLASS:None, KEY.TEXT:None }

    fmpd_code_key = dict(flight_management_panel_dom_)
    fmpd_code_key[KEY.CLASS] = DOM_CLASS.FMP_INFORMATION_NON_STATUS_KEY
    fmpd_code_key[KEY.TEXT] = STRING.FLIGHT_CODE_KEY
    fmpd_code_value = dict(flight_management_panel_dom_)
    fmpd_code_value[KEY.CLASS] = DOM_CLASS.FMP_INFORMATION_NON_STATUS_VALUE
    fmpd_code_value[KEY.TEXT] = arrivaldeparture_flight.flight_code

    fmpd_airport_key = dict(flight_management_panel_dom_)
    fmpd_airport_key[KEY.CLASS] = DOM_CLASS.FMP_INFORMATION_NON_STATUS_KEY
    fmpd_airport_key[KEY.TEXT] = STRING.FLIGHT_AIRPORT_KEY
    fmpd_airport_value = dict(flight_management_panel_dom_)
    fmpd_airport_value[KEY.CLASS] = DOM_CLASS.FMP_INFORMATION_NON_STATUS_VALUE
    fmpd_airport_value[KEY.TEXT] = arrivaldeparture_flight.airport

    fmpd_day_key = dict(flight_management_panel_dom_)
    fmpd_day_key[KEY.CLASS] = DOM_CLASS.FMP_INFORMATION_NON_STATUS_KEY
    fmpd_day_key[KEY.TEXT] = STRING.FLIGHT_DAY_KEY
    fmpd_day_value = dict(flight_management_panel_dom_)
    fmpd_day_value[KEY.CLASS] = DOM_CLASS.FMP_INFORMATION_NON_STATUS_VALUE
    fmpd_day_value[KEY.TEXT] = arrivaldeparture_flight.day

    fmpd_schedule_key = dict(flight_management_panel_dom_)
    fmpd_schedule_key[KEY.CLASS] = DOM_CLASS.FMP_INFORMATION_NON_STATUS_KEY
    fmpd_schedule_key[KEY.TEXT] = STRING.FLIGHT_SCHEDULE_KEY
    fmpd_schedule_value = dict(flight_management_panel_dom_)
    fmpd_schedule_value[KEY.CLASS] =\
        DOM_CLASS.FMP_INFORMATION_NON_STATUS_VALUE
    fmpd_schedule_value[KEY.TEXT] = arrivaldeparture_flight.scheduled_datetime

    """ This is actually a 3 dimensional array. """
    flight_management_panel_dom = [[
        [fmpd_code_key, fmpd_code_value],
        [fmpd_airport_key, fmpd_airport_value]],
        [[fmpd_day_key, fmpd_day_value],
        [fmpd_schedule_key, fmpd_schedule_value]
    ]]

    dictionary = {}
    dictionary[KEY.FMP_NON_STATUS_DOM_PARAMETERS] =\
        flight_management_panel_dom
    dictionary[KEY.FMP_NON_STATUS_FLIGHT_ID] = arrivaldeparture_flight.id
    dictionary[KEY.FMP_NON_STATUS_LANE] =\
        arrivaldeparture_flight.lane.id if arrivaldeparture_flight.lane\
            != None else None
    dictionary[KEY.FMP_NON_STATUS_ONLINE_ATCS] =\
        list(arrivaldeparture_flight.online_atcs.values_list("id", flat=True))
    dictionary[KEY.FMP_STATUS] = get_flight_status_as_a_string(
        dictionary[KEY.FMP_NON_STATUS_ONLINE_ATCS],
        dictionary[KEY.FMP_NON_STATUS_LANE]
    )

    return dictionary

"""
Function to return string so that `ArrivalDepartureFlight.status` can be
easily understandable.
"""
def get_flight_status_as_a_string(with_atc, with_lane):
    if not bool(with_atc) and not bool(with_lane):
        return STRING.NO_ATC_AND_NO_LANE
    elif not bool(with_atc) and bool(with_lane):
        return STRING.NO_ATC
    elif bool(with_atc) and not bool(with_lane):
        return STRING.NO_LANE

    return STRING.SET

def set_flight_management_panel_non_status_and_status(
    dictionary,
    non_status_dom,
    status
):
    dictionary[KEY.FMP_NON_STATUS_DOM_PARAMETERS] = non_status_dom
    dictionary[KEY.FMP_STATUS] = status

    return dictionary