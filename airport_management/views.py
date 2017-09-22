from .models import AirTrafficController, ArrivalFlight, DepartureFlight, Lane
from .src.consts import AOD, DOM_ID, KEY, MODAL_FIELD, STRING, VALUE
from .src.database_operation import\
    get_earliest_object_from_a_day, \
    get_latest_datetime_from_a_model, \
    get_list_from_object_field
from .src.specific_functions import \
    create_pagination_return_page_and_number_of_pages, \
    generate_flight_management_panel_dom_parameters, \
    set_flight_management_panel_non_status_and_status
from django.shortcuts import render

def index(request):
    """ Create paginations. """
    flight_table_paginations = {}
    flight_table_paginations_parameters = [
        [KEY.ARRIVAL_FLIGHT_TABLE_PAGINATION, ArrivalFlight],
        [KEY.DEPARTURE_FLIGHT_TABLE_PAGINATION, DepartureFlight]
    ]

    """
    Create arrival flight table pagination and departure flight pagination.
    """
    for flight_table_pagination_parameters in\
        flight_table_paginations_parameters:
        flight_table_paginations[flight_table_pagination_parameters[0]] =\
            create_pagination_return_page_and_number_of_pages(
                flight_table_pagination_parameters[1],
                MODAL_FIELD.SCHEDULED_DATETIME,
                VALUE.PAGINATION_OBJECTS_COUNT_PER_PAGE
            )

    """
    For the initial page, set the flight management panel only to display the
    earliest flight from the latest recorded day. This could be changed based
    on the preference.
    """
    latest_datetime_from_arrivalflight = get_latest_datetime_from_a_model(
        ArrivalFlight,
        MODAL_FIELD.SCHEDULED_DATETIME
    )

    """
    Get the earliest `ArrivalFlight` document from the latest day as the fist
    document shown in the flight management panel.
    """
    earliest_arrivalflight_from_the_latest_day =\
        get_earliest_object_from_a_day(
            ArrivalFlight,
            MODAL_FIELD.SCHEDULED_DATETIME,
            latest_datetime_from_arrivalflight
        )

    """ Create parameters for flight management panel DOM. """
    flight_management_panel_initial_dom =\
        generate_flight_management_panel_dom_parameters(
            earliest_arrivalflight_from_the_latest_day
        )

    """
    Dictionary that will be used to render views. Dictionary for initially
    displayed flight management panel.

    PENDING: Could be refactored alongside with the `table_requests_flight()`
    function.
    """
    parameters = {}
    parameters = set_flight_management_panel_non_status_and_status(
        parameters,
        flight_management_panel_initial_dom\
            [KEY.FMP_NON_STATUS_DOM_PARAMETERS],
        flight_management_panel_initial_dom[KEY.FMP_STATUS]
    )

    """ Assigning airport manager into client's render view. """
    parameters[KEY.AIRPORT_MANAGER] = request.user

    """ Assigning all ATCs into client's render view. """
    parameters[KEY.ATC_OBJECTS] = AirTrafficController.objects.all()

    """ Assigning all Lanes into client's render view. """
    parameters[KEY.LANE_OBJECTS] = Lane.objects.all();

    """ Parameters to help set initial flight online ATCs form. """
    parameters[KEY.FLIGHT_ONLINE_ATC_FORM_ARRIVALDEPARTURE] = AOD.ARRIVAL
    parameters[KEY.FLIGHT_ONLINE_ATC_FORM_FLIGHT_ID] =\
        earliest_arrivalflight_from_the_latest_day.id
    parameters[KEY.FLIGHT_ONLINE_ATC_FORM_FLIGHT_ONLINE_ATCS_ID] =\
        get_list_from_object_field(
            earliest_arrivalflight_from_the_latest_day.online_atcs, "id")

    """ Parameters to help to set initial flight lane form. """
    parameters[KEY.FLIGHT_LANE_FORM_ARRIVALDEPARTURE] =\
        parameters[KEY.FLIGHT_ONLINE_ATC_FORM_ARRIVALDEPARTURE]
    parameters[KEY.FLIGHT_LANE_FORM_FLIGHT_ID] =\
        parameters[KEY.FLIGHT_ONLINE_ATC_FORM_FLIGHT_ID]
    parameters[KEY.FLIGHT_LANE_FORM_FLIGHT_ONLINE_ATCS] =\
        "" if earliest_arrivalflight_from_the_latest_day.lane ==\
            None else earliest_arrivalflight_from_the_latest_day.lane.id

    """ Both arrival flight table and departure flight table properties. """
    parameters[KEY.TABLES_PROPERTIES] = [
        {
            KEY.ARRIVALDEPARTUREFLIGHT_OBJECTS:
                flight_table_paginations\
                    [KEY.ARRIVAL_FLIGHT_TABLE_PAGINATION][KEY.OBJECTS],
            KEY.TABLE_PAGINATION_NUMBER_OF_PAGES:
                flight_table_paginations\
                    [KEY.ARRIVAL_FLIGHT_TABLE_PAGINATION]\
                    [KEY.NUMBER_OF_PAGES],
            KEY.TABLE_TITLE: STRING.ARRIVAL_TABLE_TITLE,
            KEY.TABLE_ID: DOM_ID.ARRIVAL_FLIGHT_TABLE,
            KEY.TABLE_ERROR_ID: DOM_ID.ARRIVAL_FLIGHT_TABLE_ERROR,
            KEY.TABLE_PAGINATION_ID: DOM_ID.ARRIVAL_FLIGHT_TABLE_PAGINATION,
            KEY.TABLE_PAGINATION_NUMBER_OF_PAGES_ID:
                DOM_ID.ARRIVAL_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES,
            KEY.TABLE_REQUESTING_ID:
                DOM_ID.ARRIVAL_FLIGHT_TABLE_REQUESTING
        },
        {
            KEY.ARRIVALDEPARTUREFLIGHT_OBJECTS:
                flight_table_paginations\
                    [KEY.DEPARTURE_FLIGHT_TABLE_PAGINATION][KEY.OBJECTS],
            KEY.TABLE_PAGINATION_NUMBER_OF_PAGES:
                flight_table_paginations\
                    [KEY.DEPARTURE_FLIGHT_TABLE_PAGINATION]\
                    [KEY.NUMBER_OF_PAGES],
            KEY.TABLE_TITLE: STRING.DEPARTURE_TABLE_TITLE,
            KEY.TABLE_ID: DOM_ID.DEPARTURE_FLIGHT_TABLE,
            KEY.TABLE_ERROR_ID: DOM_ID.DEPARTURE_FLIGHT_TABLE_ERROR,
            KEY.TABLE_PAGINATION_ID:
                DOM_ID.DEPARTURE_FLIGHT_TABLE_PAGINATION,
            KEY.TABLE_PAGINATION_NUMBER_OF_PAGES_ID:
                DOM_ID.DEPARTURE_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES,
            KEY.TABLE_REQUESTING_ID:
                DOM_ID.DEPARTURE_FLIGHT_TABLE_REQUESTING
        }
    ]

    """ Render index.html with the dictionary as parameter. """
    return render(request, "airport_management/index.html", parameters)