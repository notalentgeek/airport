""" Deals with views for HTTP requests. """

from .models import AirTrafficController, ArrivalFlight, DepartureFlight
from .src.consts import AOD, DOM_ID, KEY, MODAL_FIELD, VALUE
from .src.specific_functions import \
    create_pagination_return_page_and_number_of_pages, \
    generate_flight_management_panel_dom_parameters, \
    set_flight_management_panel_non_status_and_status
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse
from json import dumps

""" Processing HTTP request from AngularJS. """
def table_requests_flight(request):
    """ The `id` of the arrival and departure flight we are looking for. """
    flight_id = request.GET.get(KEY.FLIGHT_ID, "")

    """
    `requested_table` is either `1` or `2`. `1` refers to arrival flight
    table, while `2` refers to departure flight.
    """
    requested_table = request.GET.get(KEY.REQUESTED_TABLE, "0")

    """ We need to coerce the value first to integer. """
    flight = None
    if str(requested_table) == str(AOD.ARRIVAL):
        flight = ArrivalFlight.objects.get(pk=flight_id)
    elif str(requested_table) == str(AOD.DEPARTURE):
        flight = DepartureFlight.objects.get(pk=flight_id)

    flight_management_panel_initial_dom =\
        generate_flight_management_panel_dom_parameters(flight)

    """ Get the template HTML file for the flight management panel. """
    flight_management_panel_inforation_template =\
        get_template(
            "airport_management/flight_management_panel_information.html"
        )

    """ Setting up DOM parameters. """
    parameters = {}
    parameters = set_flight_management_panel_non_status_and_status(
        parameters,
        flight_management_panel_initial_dom\
            [KEY.FMP_NON_STATUS_DOM_PARAMETERS],
        flight_management_panel_initial_dom[KEY.FMP_STATUS]
    )

    """
    Render the template with some parameter. Fill the HTML with parameters.
    """
    flight_management_panel_html =\
        flight_management_panel_inforation_template.render(
            parameters,
            request
        )

    """ This is the dictionary that will be returned. """
    dictionary = {}
    dictionary[KEY.FMP_DOM] = flight_management_panel_html
    dictionary[KEY.FMP_NON_STATUS_LANE] =\
        flight_management_panel_initial_dom[KEY.FMP_NON_STATUS_LANE]
    dictionary[KEY.FMP_NON_STATUS_ONLINE_ATCS] =\
        flight_management_panel_initial_dom[KEY.FMP_NON_STATUS_ONLINE_ATCS]

    return HttpResponse(dumps(dictionary))

def pagination_requests_flight_table(request):
    """ Closure. """
    def pagination_request_flight_table_(model_objects, pagination_page):
        model_paginations = create_pagination_return_page_and_number_of_pages(
            model_objects,
            MODAL_FIELD.SCHEDULED_DATETIME,
            VALUE.PAGINATION_OBJECTS_COUNT_PER_PAGE,
            pagination_page
        )

        # Set the necessary parameters for the inner table template.
        dom_id = None
        if model_objects == ArrivalFlight:
            dom_id = DOM_ID.ARRIVAL_FLIGHT_TABLE_PAGINATION
        if model_objects == DepartureFlight:
            dom_id = DOM_ID.DEPARTURE_FLIGHT_TABLE_PAGINATION

        table_template = get_template("airport_management/inner_table.html")
        table_html = table_template.render({
            KEY.DOM_ID: dom_id,
            KEY.OBJECTS: model_paginations[KEY.OBJECTS]
        }, request)

        dictionary = {}
        dictionary[KEY.TABLE_HTML] = table_html
        dictionary[KEY.NUMBER_OF_PAGES] =\
            model_paginations[KEY.NUMBER_OF_PAGES]

        return HttpResponse(dumps(dictionary))

    """ The pagination page the application is looking for. """
    pagination_page = request.GET.get(KEY.REQUESTED_TABLE_PAGINATION_PAGE, "")

    """
    `requested_table` is either `1` or `2`. `1` refers to arrival flight
    table, while `2` refers to departure flight.
    """
    requested_table = request.GET.get(KEY.REQUESTED_TABLE, "0")

    """ We need to coerce the value first to integer. """
    if str(requested_table) == str(AOD.ARRIVAL):
        return pagination_request_flight_table_(
            ArrivalFlight,
            pagination_page
        )
    elif str(requested_table) == str(AOD.DEPARTURE):
        return pagination_request_flight_table_(
            DepartureFlight,
            pagination_page
        )