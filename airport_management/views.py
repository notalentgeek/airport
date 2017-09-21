from .models import AirTrafficController, ArrivalFlight, DepartureFlight
from .consts import AOD, DOM_CLASS, DOM_ID, KEY, MODAL_FIELD, STRING, VALUE
from collections import namedtuple
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.core import serializers
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Max, Min
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse
from django.utils.timezone import localtime
from enum import Enum
from json import dumps

""" Non-transit views. """
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

    """ Assigning all ATCs in to client's render view. """
    parameters[KEY.ATC_OBJECTS] = AirTrafficController.objects.all()

    """ Parameters to help set initial flight online ATCs form. """
    parameters[KEY.FLIGHT_ATC_FORM_ARRIVALDEPARTURE] = AOD.ARRIVAL
    parameters[KEY.FLIGHT_ATC_FORM_FLIGHT_ID] =\
        earliest_arrivalflight_from_the_latest_day.id
    parameters[KEY.FLIGHT_ATC_FORM_FLIGHT_ONLINE_ATCS] =\
        get_list_from_object_field(
            earliest_arrivalflight_from_the_latest_day.online_atcs, "id")

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

""" Transit views. """

def airport_manager_login_and_registration_form(request):
    if request.POST[KEY.AIRPORT_MANAGER_LOGIN_OR_REGISTER_BUTTON] ==\
        STRING.LOGIN:
        return login_airport_manager(request)
    elif request.POST[KEY.AIRPORT_MANAGER_LOGIN_OR_REGISTER_BUTTON] ==\
        STRING.REGISTER:
        return register_airport_manager(request)

    return HttpResponseRedirect(reverse("airport_management:index"))

def check_atc_code_existence(request):
    return check_existence(request, KEY.ATC_CODE, AirTrafficController,
        MODAL_FIELD.ATC_CODE)

def check_airport_manager_name_existence(request):
    return check_existence(request, KEY.AIRPORT_MANAGER_NAME, User,
        MODAL_FIELD.AIRPORT_MANAGER_NAME)

def login_airport_manager(request):
    airport_manager = authenticate(
        username=request.POST[KEY.AIRPORT_MANAGER_NAME_INPUT],
        password=request.POST[KEY.AIRPORT_MANAGER_PASSWORD_INPUT]
    )

    """ For correct and wrong password. """
    if airport_manager is not None:
        if airport_manager.is_active and not airport_manager.is_superuser:
            login(request, airport_manager)
            return HttpResponseRedirect(reverse("airport_management:index"))

    """
    Sent wrong password parameters to the views. With this line below
    index.html will be rendered as the previously inputted password was
    wrong.

    CAUTION: This will also executed when user tried to log into super user
    account.
    """
    messages.error(request, "wrong_password")
    return HttpResponseRedirect(reverse("airport_management:index"))

    """ This is the recommended way to re-direct user after failed login. """
    #return render(request, "airport_management/index.html", {
    #    "user":request.user, "wrong_password":True })

def logout_airport_manager(request):
    logout(request)
    return HttpResponseRedirect(reverse("airport_management:index"))

def register_airport_manager(request):
    try:
        """ Register airport manager. """
        username=request.POST[KEY.AIRPORT_MANAGER_NAME_INPUT]
        password=request.POST[KEY.AIRPORT_MANAGER_PASSWORD_INPUT]
        airport_manager = User.objects.create_user(username,
            password=password)

        """
        Add the newly created airport manager into airport manager group.
        """
        airport_manager_group = get_or_create_group(
            STRING.AIRPORT_MANAGER_GROUP
        )
        airport_manager.groups.add(airport_manager_group)
        airport_manager.save()
    except IntegrityError as error:
        print(error)

    return HttpResponseRedirect(reverse("airport_management:index"))

def register_atc(request):
    try:
        code = request.POST[KEY.ATC_CODE_INPUT]
        first_name = request.POST[KEY.ATC_FIRST_NAME_INPUT]
        last_name = request.POST[KEY.ATC_LAST_NAME_INPUT]

        AirTrafficController.objects.create(
            code=code,
            first_name=first_name,
            last_name=last_name
        )
    except IntegrityError as error:
        print(error)

    return HttpResponseRedirect(reverse("airport_management:index"))

""" Functions to process HTTP request from client. """

""" Dealing with client request to add ATCs in a flight object. """
def flight_atc_form(request):
    arrivaldeparture = request.POST[KEY.FLIGHT_ATC_FORM_ARRIVALDEPARTURE]
    flight_id = request.POST[KEY.FLIGHT_ATC_FORM_FLIGHT_ID]
    online_atcs = request.POST.getlist(KEY.FLIGHT_ONLINE_ATC_CHECK_BOXES)

    model = None
    if str(arrivaldeparture) == str(AOD.ARRIVAL):
        model = ArrivalFlight
    if str(arrivaldeparture) == str(AOD.DEPARTURE):
        model = DepartureFlight

    flight = model.objects.get(pk=flight_id)
    flight.online_atcs.clear()
    
    if len(online_atcs) > 0:
        for online_atc in online_atcs:
            atc = AirTrafficController.objects.get(pk=online_atc)
            print(atc)
            flight.online_atcs.add(atc)

    return HttpResponseRedirect(reverse("airport_management:index"))

""" Processing HTTP request from AngularJS. """
def table_requests_flight(request):
    """ The `id` of the arrival and departure flight we are looking for. """
    flight_id = request.GET.get(KEY.FLIGHT_ID, "")

    """
    `requested_table` is either `1` or `2`. `1` refers to arrival flight
    table, while `2` refers to departure flight.
    """
    requested_table = request.GET.get(KEY.REQUESTED_TABLE, "0")

    flight = None

    """ We need to coerce the value first to integer. """
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
    set_flight_management_panel_non_status_and_status
    dictionary[KEY.FMP_DOM] =\
        flight_management_panel_html
    dictionary[KEY.FMP_NON_STATUS_ONLINE_ATCS] =\
        flight_management_panel_initial_dom[KEY.FMP_NON_STATUS_ONLINE_ATCS]

    return HttpResponse(dumps(dictionary))

def pagination_request_flight_table(request):
    """ Closure. """
    def pagination_request_flight_table_(model_objects, pagination_page):
        model_paginations = create_pagination_return_page_and_number_of_pages(
            model_objects,
            MODAL_FIELD.SCHEDULED_DATETIME,
            VALUE.PAGINATION_OBJECTS_COUNT_PER_PAGE,
            pagination_page
        )

        table_template = get_template("airport_management/inner_table.html")
        table_html = table_template.render({
            "flight_objects":model_paginations["objects"]
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
    if int(requested_table) == AOD.ARRIVAL:
        return pagination_request_flight_table_(
            ArrivalFlight,
            pagination_page
        )
    elif int(requested_table) == AOD.DEPARTURE:
        return pagination_request_flight_table_(
            DepartureFlight,
            pagination_page
        )

""" Non-view functions. """

"""
Function to check existence of a value in an attribute in a model table.
"""
def check_existence(
    request,
    key_name,       # Key name from the client.
    model,          # Model to look up.
    key_name_filter # Key name from the model.
):
    value = request.GET.get(key_name, "")
    return HttpResponse(model.objects.filter(**{ key_name_filter:value })\
        .exists())

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

""" A function to create or get group (Django). """
def create_or_get_group(group_name):
    try:
        return Group.objects.create(name=group_name)
    except IntegrityError as error:
        return Group.objects.get(name=group_name)

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
    dictionary[KEY.FMP_NON_STATUS_FLIGHT_LANE] = arrivaldeparture_flight.lane
    dictionary[KEY.FMP_NON_STATUS_ONLINE_ATCS] =\
        list(arrivaldeparture_flight.online_atcs.values_list("id", flat=True))
    dictionary[KEY.FMP_STATUS] = get_flight_status_as_a_string(
        arrivaldeparture_flight.online_atcs, arrivaldeparture_flight.lane)

    return dictionary

""" A function to get earliest date and time from a field in a model. """
def get_earliest_datetime_from_a_model(
    model,
    field_name # The date and time field of which the earliest date and time
               # will be found.
):
    return model.objects.aggregate(Min(field_name))\
        ["{}{}".format(field_name, "__min")]

""" Function to get the earliest document from a day. """
def get_earliest_object_from_a_day(model, field_name, datetime):
    return model.objects.filter(**{
        field_name + "__year":datetime.year,
        field_name + "__month":datetime.month,
        field_name + "__day":datetime.day
    }).order_by(field_name)[0]

"""
Function to return string so that `ArrivalDepartureFlight.status` can be
easily understandable.
"""
def get_flight_status_as_a_string(with_atc, with_lane):
    if not with_atc and not with_lane:
        return STRING.NO_ATC_AND_NO_LANE
    elif not with_atc and with_lane:
        return STRING.NO_ATC
    elif with_atc and not with_lane:
        return STRING.NO_LANE

    return ""

""" A function to get latest date and time from a field in a model. """
def get_latest_datetime_from_a_model(
    model,
    field_name # The date and time field of which the latest date and time
               # will be found.
):
    return model.objects.aggregate(Max(field_name))\
        ["{}{}".format(field_name, "__max")]

""" Get list from object field in a model. """
def get_list_from_object_field(model_object, field):
    return list(model_object.all().values_list(field, flat=True))

def set_flight_management_panel_non_status_and_status(
    dictionary,
    non_status_dom,
    status
):
    dictionary[KEY.FMP_NON_STATUS_DOM_PARAMETERS] = non_status_dom
    dictionary[KEY.FMP_NON_STATUS_ONLINE_ATCS] = status

    return dictionary

""" Decorator function. """

"""
This function was meant for view that can only be accessed by certain group.
However, because there is only one kind of `User` in this prototype, this
function is not currently being used.
"""
def airport_manager_login_required(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated() and\
            user.groups.filter(name=AIRPORT_MANAGER_GROUP).exists():
            return function(request, *args, **kwargs)
        else:
            return HttpResponse("you are not allowed to see this web page")

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap