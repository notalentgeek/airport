from .consts import AOD, CSS, KEY
from .models import AirTrafficController, ArrivalFlight, DepartureFlight
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

"""
Airport manager user group. This is not used in this prototype. Initially, I
want to register air traffic controller (ATC) as `User` as well, but for now it
is too complicated.
"""
AIRPORT_MANAGER_GROUP = "airport_manager_group"

# Field name used to sort models historically.
DATETIME_FIELD_FOR_ARRIVALDEPARTURE_MODELS = "scheduled_datetime"

# The amount of objects in each paginations.
PAGINATION_OBJECTS_COUNT = 100

"""
PENDING:Practically this application will not work with empty database. Hence
please make sure that the migrations happen with the fixtures.
"""

# Create your views here.

# Non-transit views.
def index(request):
    # Informations for flight management panel.

    """
    For the initial page set the flight management panel to only display the
    earliest flight from the latest day. This could be changed based on
    preference though.
    """
    latest_datetime_from_arrivalflight = get_latest_datetime_from_a_model(
        ArrivalFlight, DATETIME_FIELD_FOR_ARRIVALDEPARTURE_MODELS)

    """
    Get the earliest `ArrivalFlight` document from the latest day as the first
    document shown in the flight management panel.
    """
    earliest_arrivalflight_from_latest_day = get_earliest_document_from_a_day(
        ArrivalFlight,
        DATETIME_FIELD_FOR_ARRIVALDEPARTURE_MODELS,
        latest_datetime_from_arrivalflight
    )

    flight_management_panel_initial_dom = generate_flight_management_panel_dom(
        earliest_arrivalflight_from_latest_day)

    # Informations for flight table.

    # Create paginations.
    arrivalflight_paginations =\
        create_pagination_return_page_and_num_pages(
            ArrivalFlight,
            DATETIME_FIELD_FOR_ARRIVALDEPARTURE_MODELS,
            PAGINATION_OBJECTS_COUNT
        )
    departureflight_paginations =\
        create_pagination_return_page_and_num_pages(
            DepartureFlight,
            DATETIME_FIELD_FOR_ARRIVALDEPARTURE_MODELS,
            PAGINATION_OBJECTS_COUNT
        )

    # Tables properties (arrival table and departure table).
    tables_properties = [
        {
            "flight_objects":arrivalflight_paginations["objects"],
            "number_of_pages":arrivalflight_paginations["number_of_pages"],
            "table_set_container_id":\
                CSS.ARRIVAL_FLIGHT_TABLE_SET_CONTAINER_ID,
            "table_error_id":CSS.ARRIVAL_FLIGHT_TABLE_ERROR_ID,
            "table_id":CSS.ARRIVAL_FLIGHT_TABLE_ID,
            "table_pagination_id":CSS.ARRIVAL_FLIGHT_TABLE_PAGINATION_ID,
            "table_requesting_id":CSS.ARRIVAL_FLIGHT_TABLE_REQUESTING_ID,
            "table_title":"arrival table"
        },
        {
            "flight_objects":departureflight_paginations["objects"],
            "number_of_pages":departureflight_paginations["number_of_pages"],
            "table_set_container_id":\
                CSS.DEPARTURE_FLIGHT_TABLE_SET_CONTAINER_ID,
            "table_error_id":CSS.DEPARTURE_FLIGHT_TABLE_ERROR_ID,
            "table_id":CSS.DEPARTURE_FLIGHT_TABLE_ID,
            "table_pagination_id":CSS.DEPARTURE_FLIGHT_TABLE_PAGINATION_ID,
            "table_requesting_id":CSS.DEPARTURE_FLIGHT_TABLE_REQUESTING_ID,
            "table_title":"departure table"
        }
    ]

    return render(request, "airport_management/index.html", {
        "atcs":AirTrafficController.objects.all(),
        "flight_management_panel_initial_doms":\
            flight_management_panel_initial_dom["doms"],
        "flight_management_panel_initial_status_dom":\
            flight_management_panel_initial_dom["status"],
        "tables_properties":tables_properties,
        "airport_manager":request.user
    })

# Transit views.

# Dealing with ATC.
def check_atc_code_existence(request):
    return check_existence(request, KEY.ATC_CODE, AirTrafficController, "code")

def register_atc(request):
    try:
        code = request.POST[KEY.ATC_FORM_CODE_INPUT]
        first_name = request.POST[KEY.ATC_FORM_FIRST_NAME_INPUT]
        last_name = request.POST[KEY.ATC_FORM_LAST_NAME_INPUT]

        AirTrafficController.objects.create(
            code=code,
            first_name=first_name,
            last_name=last_name
        )
    except IntegrityError as error:
        print(error)

    return HttpResponseRedirect(reverse("airport_management:index"))

# Dealing with the airport manager (the main user for this application).
def check_airport_manager_name_existence(request):
    return check_existence(request, KEY.AIRPORT_MANAGER_NAME, User,
        "username")

def login_or_register_airport_manager(request):
    if request.POST[KEY.AIRPORT_MANAGER_SUBMIT_BUTTON] == "login":
        return login_airport_manager(request)
    elif request.POST[KEY.AIRPORT_MANAGER_SUBMIT_BUTTON] == "register":
        return register_airport_manager(request)

    return HttpResponseRedirect(reverse("airport_management:index"))

def login_airport_manager(request):
    airport_manager = authenticate(
        username=request.POST[KEY.AIRPORT_MANAGER_NAME_INPUT],
        password=request.POST[KEY.AIRPORT_MANAGER_PASSWORD_INPUT]
    )

    # For correct and wrong password.
    if airport_manager is not None:
        if airport_manager.is_active:
            login(request, airport_manager)
            return HttpResponseRedirect(reverse("airport_management:index"))
    else:
        """
        Sent wrong password parameters to the views. With this line below
        index.html will be rendered as the previously inputted password was
        wrong.
        """
        messages.error(request, "wrong_password")
        return HttpResponseRedirect(reverse("airport_management:index"))

        # This is the recommended way to re-direct user after failed login.
        #return render(request, "airport_management/index.html", {
        #    "user":request.user, "wrong_password":True })

def register_airport_manager(request):
    try:
        # Register airport manager.
        username=request.POST[KEY.AIRPORT_MANAGER_NAME_INPUT]
        password=request.POST[KEY.AIRPORT_MANAGER_PASSWORD_INPUT]
        airport_manager = User.objects.create_user(username, password=password)

        # Add the newly created airport manager into airport manager group.
        airport_manager_group = get_or_create_group(AIRPORT_MANAGER_GROUP)
        airport_manager.groups.add(airport_manager_group)
        airport_manager.save()
    except IntegrityError as error:
        print(error)

    return HttpResponseRedirect(reverse("airport_management:index"))

def logout_airport_manager(request):
    logout(request)
    return HttpResponseRedirect(reverse("airport_management:index"))

# Processing HTTP request from AngularJS.
def table_request_flight(request):
    # The `id` of the arrival and departure flight we are looking for.
    flight_id = request.GET.get(KEY.FLIGHT_ID, "")

    """
    `requested_table` is either `1` or `2`. `1` refers to arrival flight table,
    while `2` refers to departure flight.
    """
    requested_table = request.GET.get(KEY.REQUESTED_TABLE, "0")

    # We need to coerce the value first to integer.
    if int(requested_table) == AOD.ARRIVAL:
        flight = ArrivalFlight.objects.get(pk=flight_id)
    elif int(requested_table) == AOD.DEPARTURE:
        flight = DepartureFlight.objects.get(pk=flight_id)

    flight_management_panel_initial_doms = generate_flight_management_panel_dom(
        flight)

    # Get the template HTML file for the flight management panel.
    flight_management_panel_template =\
        get_template("airport_management/flight_management_panel.html")

    # Render the template with some parameter.
    flight_management_panel_html = flight_management_panel_template.render({
        "flight_management_panel_initial_doms":\
            flight_management_panel_initial_doms["doms"],
        "flight_management_panel_initial_status_doms":\
            flight_management_panel_initial_doms["status"]
    }, request)

    return HttpResponse(flight_management_panel_html)

def pagination_request_flight_table(request):
    # Closure.
    def pagination_request_flight_table_(model_objects, pagination_page):
        model_paginations = create_pagination_return_page_and_num_pages(
            model_objects,
            DATETIME_FIELD_FOR_ARRIVALDEPARTURE_MODELS,
            PAGINATION_OBJECTS_COUNT,
            pagination_page
        )

        table_template = get_template("airport_management/paginated_table.html")
        table_html = table_template.render({
            "flight_objects":model_paginations["objects"]
        }, request)

        dictionary = {}
        dictionary[KEY.TABLE_HTML] = table_html
        dictionary[KEY.NUMBER_OF_PAGES] = model_paginations["number_of_pages"]

        return HttpResponse(dumps(dictionary))

    # The pagination page the application is looking for.
    pagination_page = request.GET.get(KEY.REQUESTED_PAGINATION_PAGE, "")

    """
    `requested_table` is either `1` or `2`. `1` refers to arrival flight table,
    while `2` refers to departure flight.
    """
    requested_table = request.GET.get(KEY.REQUESTED_TABLE, "0")
    # We need to coerce the value first to integer.
    if int(requested_table) == AOD.ARRIVAL:
        return pagination_request_flight_table_(ArrivalFlight,
            pagination_page)
    elif int(requested_table) == AOD.DEPARTURE:
        return pagination_request_flight_table_(DepartureFlight,
            pagination_page)

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

# Non-view functions.

# Function to check existence based on one field and its value.
def check_existence(
    request,         # Request object.
    key_name,        # Key name from the client.
    model,           # Model to look up.
    key_name_filter, # Key name from the model.
):
    value = request.GET.get(key_name, "")
    return HttpResponse(model.objects.filter(**{ key_name_filter:value })
        .exists())

def create_pagination_return_page_and_num_pages(
    model,
    order_field, # Table of which pagination will be sorted into (to prevent
                 # warning).
    amount,
    returned_page=1
):
    paginator = Paginator(model.objects.all().order_by(order_field), amount)
    dictionary = {}
    dictionary["objects"] = paginator.page(returned_page).object_list
    dictionary["number_of_pages"] = paginator.num_pages

    return dictionary

# Function to generate DOM elements for flight management panel.
def generate_flight_management_panel_dom(arrivaldeparture_flight):
    flight_management_panel_dom_fragment = { "class":None, "text":None }

    fmpdf_code_key = dict(flight_management_panel_dom_fragment)
    fmpdf_code_key["class"] = CSS.FLIGHT_MANAGEMENT_PANEL_KEY_CLASS
    fmpdf_code_key["text"] = "code:"
    fmpdf_code_value = dict(flight_management_panel_dom_fragment)
    fmpdf_code_value["class"] = CSS.FLIGHT_MANAGEMENT_PANEL_VALUE_CLASS
    fmpdf_code_value["text"] = arrivaldeparture_flight.flight_code

    fmpdf_airport_key = dict(flight_management_panel_dom_fragment)
    fmpdf_airport_key["class"] = CSS.FLIGHT_MANAGEMENT_PANEL_KEY_CLASS
    fmpdf_airport_key["text"] = "airport:"
    fmpdf_airport_value = dict(flight_management_panel_dom_fragment)
    fmpdf_airport_value["class"] = CSS.FLIGHT_MANAGEMENT_PANEL_VALUE_CLASS
    fmpdf_airport_value["text"] = arrivaldeparture_flight.airport

    fmpdf_day_key = dict(flight_management_panel_dom_fragment)
    fmpdf_day_key["class"] = CSS.FLIGHT_MANAGEMENT_PANEL_KEY_CLASS
    fmpdf_day_key["text"] = "day:"
    fmpdf_day_value = dict(flight_management_panel_dom_fragment)
    fmpdf_day_value["class"] = CSS.FLIGHT_MANAGEMENT_PANEL_VALUE_CLASS
    fmpdf_day_value["text"] = arrivaldeparture_flight.day

    fmpdf_schedule_key = dict(flight_management_panel_dom_fragment)
    fmpdf_schedule_key["class"] = CSS.FLIGHT_MANAGEMENT_PANEL_KEY_CLASS
    fmpdf_schedule_key["text"] = "schedule:"
    fmpdf_schedule_value = dict(flight_management_panel_dom_fragment)
    fmpdf_schedule_value["class"] = CSS.FLIGHT_MANAGEMENT_PANEL_VALUE_CLASS
    fmpdf_schedule_value["text"] = arrivaldeparture_flight.scheduled_datetime

    # This is actually a 3 dimensional array.
    flight_management_panel_dom = [[
        [fmpdf_code_key, fmpdf_code_value],
        [fmpdf_airport_key, fmpdf_airport_value]],
        [[fmpdf_day_key, fmpdf_day_value],
        [fmpdf_schedule_key, fmpdf_schedule_value]
    ]]

    dictionary = {}
    dictionary["doms"] = flight_management_panel_dom
    dictionary["status"] = get_flight_status_as_a_string(
        arrivaldeparture_flight.online_atc, arrivaldeparture_flight.lane)

    return dictionary

"""
Function to return string so that `ArrivalDepartureFlight.status` can be
easily understandable.
"""
def get_flight_status_as_a_string(with_atc, with_lane):
    if not with_atc and not with_lane:
        return "no atc and no lane"
    elif not with_atc and with_lane:
        return "no atc"
    elif with_atc and not with_lane:
        return "no lane"
    else:
        return ""

# Get the earliest date and time from a model.
def get_earliest_datetime_from_a_model(model, field_name):
    return model.objects.aggregate(Min(field_name))\
        ["{}{}".format(field_name, "__min")]

def get_earliest_document_from_a_day(model, field_name, datetime):
    return model.objects.filter(**{
        field_name + "__year":datetime.year,
        field_name + "__month":datetime.month,
        field_name + "__day":datetime.day
    }).order_by(field_name)[0]

# Get the latest date and time from a model.
def get_latest_datetime_from_a_model(model, field_name):
    return model.objects.aggregate(Max(field_name))\
        ["{}{}".format(field_name, "__max")]

# Get or create new group for `User`.
def get_or_create_group(group_name):
    try:
        return Group.objects.create(name=group_name)
    except IntegrityError as error:
        print(error)
        return Group.objects.get(name=group_name)