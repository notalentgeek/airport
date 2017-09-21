from .models import AirTrafficController, ArrivalFlight, DepartureFlight
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

AOD = namedtuple("AOD", "ARRIVAL DEPARTURE")
AOD = AOD(
    ARRIVAL="1",
    DEPARTURE="2"
)
DOM_CLASS = namedtuple(
    "CLASS",
    "\
        FMP_INFORMATION_NON_STATUS_KEY \
        FMP_INFORMATION_NON_STATUS_VALUE \
    "
)
DOM_CLASS = DOM_CLASS(
    FMP_INFORMATION_NON_STATUS_KEY="fmp-information-non-status-key",
    FMP_INFORMATION_NON_STATUS_VALUE="fmp-information-non-status-value"
)
DOM_ID = namedtuple(
    "DOM_ID",
    "\
        ARRIVAL_FLIGHT_TABLE \
        ARRIVAL_FLIGHT_TABLE_ERROR \
        ARRIVAL_FLIGHT_TABLE_PAGINATION \
        ARRIVAL_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES \
        ARRIVAL_FLIGHT_TABLE_REQUESTING \
        DEPARTURE_FLIGHT_TABLE \
        DEPARTURE_FLIGHT_TABLE_ERROR \
        DEPARTURE_FLIGHT_TABLE_PAGINATION \
        DEPARTURE_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES \
        DEPARTURE_FLIGHT_TABLE_REQUESTING \
    "
)
DOM_ID = DOM_ID(
    ARRIVAL_FLIGHT_TABLE="arrival-flight-table",
    ARRIVAL_FLIGHT_TABLE_ERROR="arrival-flight-table-error",
    ARRIVAL_FLIGHT_TABLE_PAGINATION="arrival-flight-table-pagination",
    ARRIVAL_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES=\
        "arrival-flight-table-pagination-number-of-pages",
    ARRIVAL_FLIGHT_TABLE_REQUESTING="arrival-flight-table-requesting",
    DEPARTURE_FLIGHT_TABLE="departure-flight-table",
    DEPARTURE_FLIGHT_TABLE_ERROR="departure-flight-table-error",
    DEPARTURE_FLIGHT_TABLE_PAGINATION="departure-flight-table-pagination",
    DEPARTURE_FLIGHT_TABLE_PAGINATION_NUMBER_OF_PAGES=\
        "departure-flight-table-pagination-number-of-pages",
    DEPARTURE_FLIGHT_TABLE_REQUESTING="departure-flight-table-requesting"
)
KEY = namedtuple(
    "KEY",
    "\
        AIRPORT_MANAGER \
        AIRPORT_MANAGER_LOGIN_OR_REGISTER_BUTTON \
        AIRPORT_MANAGER_NAME \
        AIRPORT_MANAGER_NAME_INPUT \
        AIRPORT_MANAGER_PASSWORD_INPUT \
        ARRIVALDEPARTUREFLIGHT_OBJECTS \
        ATC_CODE \
        ATC_CODE_INPUT \
        ATC_FIRST_NAME_INPUT \
        ATC_LAST_NAME_INPUT \
        ATC_OBJECTS \
        CLASS \
        FLIGHT_ATC_FORM_ARRIVALDEPARTURE \
        FLIGHT_ATC_FORM_FLIGHT_ID \
        FLIGHT_ID \
        FLIGHT_MANAGEMENT_PANEL_INITIAL_PROPERTIES \
        FLIGHT_OBJECTS \
        FLIGHT_ONLINE_ATC_CHECK_BOXES \
        FMP_DOM \
        FMP_NON_STATUS_ARRIVALDEPARTURE \
        FMP_NON_STATUS_DOM_PARAMETERS \
        FMP_NON_STATUS_FLIGHT_ID \
        FMP_NON_STATUS_FLIGHT_LANE \
        FMP_NON_STATUS_ONLINE_ATCS \
        FMP_STATUS \
        NUMBER_OF_PAGES \
        OBJECTS \
        REQUESTED_TABLE \
        TABLES_PROPERTIES \
        TABLE_ERROR_ID \
        TABLE_HTML \
        TABLE_ID \
        TABLE_PAGINATION_ID \
        TABLE_PAGINATION_NUMBER_OF_PAGES \
        TABLE_PAGINATION_NUMBER_OF_PAGES_ID \
        TABLE_TITLE \
        TABLE_REQUESTING_ID \
        TEXT \
    "
)

KEY = KEY(
    AIRPORT_MANAGER="airport_manager",
    AIRPORT_MANAGER_LOGIN_OR_REGISTER_BUTTON=\
        "airport_manager_login_or_register_button",
    AIRPORT_MANAGER_NAME="airport_manager_name",
    AIRPORT_MANAGER_NAME_INPUT="airport_manager_name_input",
    AIRPORT_MANAGER_PASSWORD_INPUT="airport_manager_password_input",
    ARRIVALDEPARTUREFLIGHT_OBJECTS="arrivaldepartureflight_objects",
    ATC_CODE="atc_code",
    ATC_CODE_INPUT="atc_code_input",
    ATC_FIRST_NAME_INPUT="atc_first_name_input",
    ATC_LAST_NAME_INPUT="atc_last_name_input",
    ATC_OBJECTS="atc_objects",
    CLASS="class",
    FLIGHT_ATC_FORM_ARRIVALDEPARTURE="flight_atc_form_arrivaldeparture",
    FLIGHT_ATC_FORM_FLIGHT_ID="flight_atc_form_flight_id",
    FLIGHT_ID="flight_id",
    FLIGHT_MANAGEMENT_PANEL_INITIAL_PROPERTIES=\
        "flight_management_panel_initial_properties",
    FLIGHT_OBJECTS="flight_objects",
    FLIGHT_ONLINE_ATC_CHECK_BOXES="flight_online_atc_check_boxes",
    FMP_DOM="fmp_dom",
    FMP_NON_STATUS_ARRIVALDEPARTURE="fmp_non_status_arrivaldeparture",
    FMP_NON_STATUS_DOM_PARAMETERS="fmp_non_status_dom_parameters",
    FMP_NON_STATUS_FLIGHT_ID="fmp_non_status_flight_id",
    FMP_NON_STATUS_FLIGHT_LANE="fmp_non_status_flight_lane",
    FMP_NON_STATUS_ONLINE_ATCS="fmp_non_status_online_atcs",
    FMP_STATUS="fmp_status",
    NUMBER_OF_PAGES="number_of_pages",
    OBJECTS="objects",
    REQUESTED_TABLE="requested_table",
    TABLES_PROPERTIES="tables_properties",
    TABLE_ERROR_ID="table_error_id",
    TABLE_HTML="table_html",
    TABLE_ID="table_id",
    TABLE_PAGINATION_ID="table_pagination_id",
    TABLE_PAGINATION_NUMBER_OF_PAGES="table_pagination_number_of_pages",
    TABLE_PAGINATION_NUMBER_OF_PAGES_ID="table_pagination_number_of_pages_id",
    TABLE_REQUESTING_ID="table_requesting_id",
    TABLE_TITLE="table_title",
    TEXT="text"
)
MODAL_FIELD = namedtuple(
    "MODEL_FIELD",
    "\
        AIRPORT_MANAGER_NAME \
        ATC_CODE \
        SCHEDULED_DATETIME \
    "
)
MODAL_FIELD = MODAL_FIELD(
    AIRPORT_MANAGER_NAME="username",
    ATC_CODE="code",
    SCHEDULED_DATETIME="scheduled_datetime"
)
STRING = namedtuple(
    "STRING",
    "\
        AIRPORT_MANAGER_GROUP \
        ARRIVAL_TABLE_TITLE \
        DEPARTURE_TABLE_TITLE \
        FLIGHT_AIRPORT_KEY \
        FLIGHT_CODE_KEY \
        FLIGHT_DAY_KEY \
        FLIGHT_SCHEDULE_KEY \
        LOGIN \
        NO_ATC \
        NO_ATC_AND_NO_LANE \
        NO_LANE \
        REGISTER \
    "
)
STRING = STRING(
    AIRPORT_MANAGER_GROUP="airport_manager_group",
    ARRIVAL_TABLE_TITLE="arrival table",
    DEPARTURE_TABLE_TITLE="departure table",
    FLIGHT_AIRPORT_KEY="airport: ",
    FLIGHT_CODE_KEY="code: ",
    FLIGHT_DAY_KEY="day: ",
    FLIGHT_SCHEDULE_KEY="schedule: ",
    LOGIN="login",
    NO_ATC="no atc",
    NO_ATC_AND_NO_LANE="no atc and not lane",
    NO_LANE="no lane",
    REGISTER="register"
)
VALUE = namedtuple("VALUE", "PAGINATION_OBJECTS_COUNT_PER_PAGE")
VALUE = VALUE(
    PAGINATION_OBJECTS_COUNT_PER_PAGE=100
)

# Non-transit views.
def index(request):
    # Create paginations.

    # Create pagination for arrival flight table.
    arrivalflight_pagination =\
        create_pagination_return_page_and_number_of_pages(
            ArrivalFlight,
            MODAL_FIELD.SCHEDULED_DATETIME,
            VALUE.PAGINATION_OBJECTS_COUNT_PER_PAGE
        )
    
    # Create pagination for departure flight table.
    departureflight_pagination = \
        create_pagination_return_page_and_number_of_pages(
            DepartureFlight,
            MODAL_FIELD.SCHEDULED_DATETIME,
            VALUE.PAGINATION_OBJECTS_COUNT_PER_PAGE
        )

    """
    For the initial page, set the flight management panel only to display the
    earliest flight from the latest recorded day. This could be changed based
    on the preference.
    """
    latest_datetime_from_arrivalflight = get_latest_datetime_from_a_model(
        ArrivalFlight, MODAL_FIELD.SCHEDULED_DATETIME)

    """
    Get the earliest `ArrivalFlight` document from the latest day as the fist
    document shown in the flight management panel.
    """
    earliest_arrivalflight_from_latest_day = get_earliest_object_from_a_day(
        ArrivalFlight,
        MODAL_FIELD.SCHEDULED_DATETIME,
        latest_datetime_from_arrivalflight
    )

    # Create flight management panel DOM.
    flight_management_panel_initial_dom =\
        generate_flight_management_panel_dom(
            earliest_arrivalflight_from_latest_day
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

    # Assigning airport manager into client's render view.
    parameters[KEY.AIRPORT_MANAGER] = request.user

    # Assigning all ATCs in to client's render view.
    parameters[KEY.ATC_OBJECTS] = AirTrafficController.objects.all()

    # Parameters to help set initial flight online ATCs form.
    parameters["flight_atc_form_arrivaldeparture"] = AOD.ARRIVAL
    parameters["flight_atc_form_flight_id"] = earliest_arrivalflight_from_latest_day.id
    parameters["flight_atc_form_flight_online_atcs"] = list(earliest_arrivalflight_from_latest_day.online_atcs.all().values_list("id", flat=True))
    #print(parameters["flight_atc_form_flight_online_atcs"]);
    #print(list(parameters["flight_atc_form_flight_online_atcs"]));


    # Both arrival flight table and departure flight table properties.
    parameters[KEY.TABLES_PROPERTIES] = [
        {
            KEY.ARRIVALDEPARTUREFLIGHT_OBJECTS:
                arrivalflight_pagination[KEY.OBJECTS],
            KEY.TABLE_PAGINATION_NUMBER_OF_PAGES:
                arrivalflight_pagination[KEY.NUMBER_OF_PAGES],
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
                departureflight_pagination[KEY.OBJECTS],
            KEY.TABLE_PAGINATION_NUMBER_OF_PAGES:
                departureflight_pagination[KEY.NUMBER_OF_PAGES],
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

    # Render index.html with the dictionary as parameter.
    return render(request, "airport_management/index.html", parameters)

# Transit views.

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

    # For correct and wrong password.
    if airport_manager is not None:
        if airport_manager.is_active and not airport_manager.is_superuser:
            login(request, airport_manager)
            return HttpResponseRedirect(reverse("airport_management:index"))

    """
    Sent wrong password parameters to the views. With this line below
    index.html will be rendered as the previously inputted password was
    wrong.

    PENDING: This will also executed when user tried to log into super user
    account.
    """
    messages.error(request, "wrong_password")
    return HttpResponseRedirect(reverse("airport_management:index"))

    # This is the recommended way to re-direct user after failed login.
    #return render(request, "airport_management/index.html", {
    #    "user":request.user, "wrong_password":True })

def logout_airport_manager(request):
    logout(request)
    return HttpResponseRedirect(reverse("airport_management:index"))

def register_airport_manager(request):
    try:
        # Register airport manager.
        username=request.POST[KEY.AIRPORT_MANAGER_NAME_INPUT]
        password=request.POST[KEY.AIRPORT_MANAGER_PASSWORD_INPUT]
        airport_manager = User.objects.create_user(username,
            password=password)

        # Add the newly created airport manager into airport manager group.
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

# Functions to process HTTP request from client.

# Dealing with client request to add ATCs in a flight object.
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

# Processing HTTP request from AngularJS.
def table_requests_flight(request):
    # The `id` of the arrival and departure flight we are looking for.
    flight_id = request.GET.get(KEY.FLIGHT_ID, "")

    """
    `requested_table` is either `1` or `2`. `1` refers to arrival flight
    table, while `2` refers to departure flight.
    """
    requested_table = request.GET.get(KEY.REQUESTED_TABLE, "0")

    flight = None

    # We need to coerce the value first to integer.
    if str(requested_table) == str(AOD.ARRIVAL):
        flight = ArrivalFlight.objects.get(pk=flight_id)
    elif str(requested_table) == str(AOD.DEPARTURE):
        flight = DepartureFlight.objects.get(pk=flight_id)

    flight_management_panel_initial_dom =\
        generate_flight_management_panel_dom(flight)

    # Get the template HTML file for the flight management panel.
    flight_management_panel_inforation_template =\
        get_template(
            "airport_management/flight_management_panel_information.html"
        )

    # Setting up DOM parameters.
    parameters = {}
    parameters = set_flight_management_panel_non_status_and_status(
        parameters,
        flight_management_panel_initial_dom\
            [KEY.FMP_NON_STATUS_DOM_PARAMETERS],
        flight_management_panel_initial_dom[KEY.FMP_STATUS]
    )

    # Render the template with some parameter. Fill the HTML with parameters.
    flight_management_panel_html =\
        flight_management_panel_inforation_template.render(
            parameters,
            request
        )

    # This is the dictionary that will be returned.
    dictionary = {}
    set_flight_management_panel_non_status_and_status
    dictionary[KEY.FMP_DOM] =\
        flight_management_panel_html
    dictionary[KEY.FMP_NON_STATUS_ONLINE_ATCS] =\
        flight_management_panel_initial_dom[KEY.FMP_NON_STATUS_ONLINE_ATCS]

    return HttpResponse(dumps(dictionary))

def pagination_request_flight_table(request):
    # Closure.
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

    # The pagination page the application is looking for.
    pagination_page = request.GET.get(KEY.REQUESTED_TABLE_PAGINATION_PAGE, "")

    """
    `requested_table` is either `1` or `2`. `1` refers to arrival flight
    table, while `2` refers to departure flight.
    """
    requested_table = request.GET.get(KEY.REQUESTED_TABLE, "0")
    # We need to coerce the value first to integer.
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

# Non-view functions.

# Function to check existence of a value in an attribute in a model table.
def check_existence(
    request,
    key_name,       # Key name from the client.
    model,          # Model to look up.
    key_name_filter # Key name from the model.
):
    value = request.GET.get(key_name, "")
    return HttpResponse(model.objects.filter(**{ key_name_filter:value })\
        .exists())

# A function to create pagination for a model.
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

# A function to create or get group (Django).
def create_or_get_group(group_name):
    try:
        return Group.objects.create(name=group_name)
    except IntegrityError as error:
        return Group.objects.get(name=group_name)

# Function to generate flight management panel DOM.
def generate_flight_management_panel_dom(arrivaldeparture_flight):
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

    # This is actually a 3 dimensional array.
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

# A function to get earliest date and time from a field in a model.
def get_earliest_datetime_from_a_model(
    model,
    field_name # The date and time field of which the earliest date and time
               # will be found.
):
    return model.objects.aggregate(Min(field_name))\
        ["{}{}".format(field_name, "__min")]

# Function to get the earliest document from a day.
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

# A function to get latest date and time from a field in a model.
def get_latest_datetime_from_a_model(
    model,
    field_name # The date and time field of which the latest date and time
               # will be found.
):
    return model.objects.aggregate(Max(field_name))\
        ["{}{}".format(field_name, "__max")]

def set_flight_management_panel_non_status_and_status(
    dictionary,
    non_status_dom,
    status
):
    dictionary[KEY.FMP_NON_STATUS_DOM_PARAMETERS] = non_status_dom
    dictionary[KEY.FMP_NON_STATUS_ONLINE_ATCS] = status

    return dictionary

# Decorator function.

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