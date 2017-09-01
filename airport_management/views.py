from .models import ArrivalFlight, DepartureFlight
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.core import serializers
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.template.loader import get_template
from django.urls import reverse
from json import dumps

AIRPORT_MANAGER_GROUP = "airport_manager"

# Create your views here.
def check_user_existence(request):
    username = request.GET.get("username", "")
    return HttpResponse(User.objects.filter(username=username).exists())

def index(request):
    # Split the flight objects into 100 documents each with `Pagination`.
    arrival_flights_paginator = Paginator(ArrivalFlight.objects.all(), 100)
    arrival_flights_paginator_page_1 =\
        arrival_flights_paginator.page(1).object_list
    departure_flights_paginator = Paginator(DepartureFlight.objects.all(), 100)
    departure_flights_paginator_page_1 =\
        departure_flights_paginator.page(1).object_list

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

    return render(request, "airport_management/index.html", {
        "properties": properties,
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
        return request_table_pagination_(ArrivalFlight.objects.all())
    elif which_pagination == "2":
        return request_table_pagination_(DepartureFlight.objects.all())

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
def get_or_create_group(group_name):
    try:
        return Group.objects.create(name=group_name)
    except IntegrityError as error:
        print(error)
        return Group.objects.get(name=group_name)
