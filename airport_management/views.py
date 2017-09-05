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
from django.template import RequestContext
from django.template.loader import get_template
from django.urls import reverse
from django.utils.timezone import localtime
from json import dumps

AIRPORT_MANAGER_GROUP = "airport_manager"
STATUS = [
    "missing atc and lane",
    "missing atc",
    "missing lane"
]

# Create your views here.
def check_air_traffic_controller_code_existence(request):
    atc_code = request.GET.get("atc_code", "")
    return HttpResponse(AirTrafficController.objects.filter(code=atc_code)
        .exists())

def check_user_existence(request):
    username = request.GET.get("username", "")
    return HttpResponse(User.objects.filter(username=username).exists())

def index(request):
    # Split the flight objects into 100 documents each with `Pagination`.
    arrival_flights_paginator = Paginator(ArrivalFlight.objects.all().order_by("sch_local_datetime"), 100)
    arrival_flights_paginator_page_1 =\
        arrival_flights_paginator.page(1).object_list
    departure_flights_paginator = Paginator(DepartureFlight.objects.all().order_by("sch_local_datetime"), 100)
    departure_flights_paginator_page_1 =\
        departure_flights_paginator.page(1).object_list

    latest_datetime = ArrivalFlight.objects.aggregate(Max("sch_local_datetime"))["sch_local_datetime__max"]
    earliest_document_from_latest_day = ArrivalFlight.objects.filter(
        sch_local_datetime__year=latest_datetime.year,
        sch_local_datetime__month=latest_datetime.month,
        sch_local_datetime__day=latest_datetime.day
    ).order_by("sch_local_datetime")[0]

    columns = [
        [
            [
                {
                    "class": "management-panel-info-text",
                    "text": "<strong>code:</strong>"
                },
                {
                    "class": "management-panel-variable-text",
                    "text": earliest_document_from_latest_day.flight_code
                }
            ],
            [
                {
                    "class": "management-panel-info-text",
                    "text": "<strong>airport:</strong>"
                },
                {
                    "class": "management-panel-variable-text",
                    "text": earliest_document_from_latest_day.airport
                }
            ]
        ],
        [
            [
                {
                    "class": "management-panel-info-text",
                    "text": "<strong>day:</strong>"
                },
                {
                    "class": "management-panel-variable-text",
                    "text": earliest_document_from_latest_day.day
                }
            ],
            [
                {
                    "class": "management-panel-info-text",
                    "text": "<strong>schedule:</strong>"
                },
                {
                    "class": "management-panel-variable-text",
                    "text": localtime(earliest_document_from_latest_day.sch_local_datetime)
                }
            ]
        ]
    ];

    status = check_flight_status(
        earliest_document_from_latest_day.online_atc,
        bool(earliest_document_from_latest_day.lane)
    )

    # Repeat table properties.
    properties = [
        {
            "data": arrival_flights_paginator_page_1,
            "id_main": "arrival-table", # For CSS purposes.
            "id_pagination": "pagination-arrival",
            "num_pages": arrival_flights_paginator.num_pages,
            "title": "arrival flights"
        },
        {
            "data": departure_flights_paginator_page_1,
            "id_main": "departure-table", # For CSS purposes.
            "id_pagination": "pagination-departure",
            "num_pages": departure_flights_paginator.num_pages,
            "title": "departure flights"
        }
    ];

    """
    PENDING: `properties` is actually used to retrieve arrival and departure
    flights data. It could be changed to better name.
    """
    return render(request, "airport_management/index.html", {
        "atcs": AirTrafficController.objects.all(),
        "columns": columns,
        "properties": properties,
        "status": status,
        "user": request.user
    })

def login_airport_manager(request):
    user = authenticate(
        username=request.POST["username"],
        password=request.POST["password"]
    )

    # For correct and wrong password.
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse("airport_management:index"))
    else:
        """
        Sent wrong password parameters to the views. With this line below
        index.html will be rendered as the previously inputted password was
        wrong.
        """
        messages.error(request, "wrong_password")
        return HttpResponseRedirect(reverse("airport_management:index"))
        #return render(request, "airport_management/index.html", {
        #    "user": request.user, "wrong_password": True })

def login_or_register_airport_manager(request):
    if request.POST["submit-button"] == "login":
        return login_airport_manager(request)
    elif request.POST["submit-button"] == "register":
        return register_airport_manager(request)

    return HttpResponseRedirect(reverse("airport_management:index"))

def logout_airport_manager(request):
    logout(request)
    return HttpResponseRedirect(reverse("airport_management:index"))

def register_airport_manager(request):
    try:
        group = get_or_create_group(AIRPORT_MANAGER_GROUP)
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.create_user(username, password=password)
        user.groups.add(group)
        user.save()
    except IntegrityError as error:
        print(error)

    return HttpResponseRedirect(reverse("airport_management:index"))

def register_atc(request):
    try:
        atc_code = request.POST["atc_code_input"]
        atc_first_name = request.POST["atc_first_name_input"]
        atc_last_name = request.POST["atc_last_name_input"]
        AirTrafficController.objects.create(
            code = atc_code,
            first_name = atc_first_name,
            last_name = atc_last_name
        )
    except IntegrityError as error:
        print(error)

    return HttpResponseRedirect(reverse("airport_management:index"))

def request_flight(request):
    # The id of the arrival or departure flight.
    id_ = request.GET.get("id", "")

    """
    `requested_table` is either `1` or `2`. `1` refers to arrival flight table,
    while `2` refers to departure flight.
    """
    requested_table = request.GET.get("requested_table", "0")

    if requested_table == "1":
        flight = ArrivalFlight.objects.get(pk=id_)
    elif requested_table == "2":
        flight = DepartureFlight.objects.get(pk=id_)

    if flight:
        columns = [
            [
                [
                    {
                        "class": "management-panel-info-text",
                        "text": "<strong>code:</strong>"
                    },
                    {
                        "class": "management-panel-variable-text",
                        "text": flight.flight_code
                    }
                ],
                [
                    {
                        "class": "management-panel-info-text",
                        "text": "<strong>airport:</strong>"
                    },
                    {
                        "class": "management-panel-variable-text",
                        "text": flight.airport
                    }
                ]
            ],
            [
                [
                    {
                        "class": "management-panel-info-text",
                        "text": "<strong>day:</strong>"
                    },
                    {
                        "class": "management-panel-variable-text",
                        "text": flight.day
                    }
                ],
                [
                    {
                        "class": "management-panel-info-text",
                        "text": "<strong>schedule:</strong>"
                    },
                    {
                        "class": "management-panel-variable-text",
                        "text": localtime(flight.sch_local_datetime)
                    }
                ]
            ]
        ];

        status = check_flight_status(
            flight.online_atc, bool(flight.lane)
        )

        template = get_template("airport_management/flight-management-panel.html")
        html = template.render({
            "columns": columns,
            "status": status
        }, request)

    return HttpResponse(html)

def request_table_pagination(request):
    page = request.GET.get("page", "")
    which_pagination = request.GET.get("which_pagination", "")

    # Closure.
    def request_table_pagination_(object_all):
        flights_paginator = Paginator(object_all, 100)
        flights_paginator_page =\
            flights_paginator.page(page).object_list

        template = get_template("airport_management/paginated-table.html")
        html = template.render({ "data_list": flights_paginator_page },
            request)

        dictionary = {
            "html": html,
            "num_pages": flights_paginator.num_pages
        }

        return HttpResponse(dumps(dictionary))

    if which_pagination == "1":
        return request_table_pagination_(ArrivalFlight.objects.all().order_by("sch_local_datetime"))
    elif which_pagination == "2":
        return request_table_pagination_(DepartureFlight.objects.all().order_by("sch_local_datetime"))

    return HttpResponse()

# Decorator function.
# Not used anymore, since there is only one type of user.
def airport_manager_login_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated() and\
            request.user.groups.filter(name=AIRPORT_MANAGER_GROUP).exists():
            return function(request, *args, **kwargs)
        else:
            return HttpResponse("you are not allowed to see this page")

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap

# Non-view function.
def check_flight_status(atc, lane):
    if not atc and not lane:
        return STATUS[0]
    elif not atc and lane:
        return STATUS[1]
    elif atc and not lane:
        return STATUS[2]
    else:
        return ""

def get_or_create_group(group_name):
    try:
        return Group.objects.create(name=group_name)
    except IntegrityError as error:
        print(error)
        return Group.objects.get(name=group_name)
