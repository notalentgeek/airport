from .models import ArrivalFlight, DepartureFlight
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

AIRPORT_MANAGER_GROUP = "airport_manager"

# Create your views here.
def check_user_existence(request):
    username = request.GET.get("username", "")
    return HttpResponse(User.objects.filter(username=username).exists())

def index(request):
    # Split the flight objects into 100 documents each with `Pagination`.
    arrival_flights_paginator = Paginator(ArrivalFlight.objects.all(), 100)
    arrival_flights = arrival_flights_paginator.page(1)
    arrival_flights_pagination_page = request.GET.get("arrival-page", 1)

    # I want to know how many documents are there in `ArrivalFlight`.
    #print(arrival_flights)
    #print(arrival_flights.object_list)
    #print(ArrivalFlight.objects.all())
    #print(type(arrival_flights))
    #print(type(ArrivalFlight.objects.all()))
    # Return 100 documents.
    print(len(arrival_flights.object_list))
    # Return all documents.
    print(ArrivalFlight.objects.all().count())
    # Arrival pagination.
    print(arrival_flights_pagination_page);

    return render(request, "airport_management/index.html", {
        "arrival_flights": arrival_flights,
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

# Decorator function.
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
