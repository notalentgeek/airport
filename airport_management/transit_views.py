"""
Transit views. The views is not necessarily display a HTML template but
just GET or POST through database.
"""

from .models import AirTrafficController, ArrivalFlight, DepartureFlight, Lane
from .src.consts import AOD, KEY, MODAL_FIELD, STRING
from .src.database_operation import check_existence, create_or_get_group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
""" Delete `HttpResponse` after developing modal form to add lane. """
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError

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

""" Function to add online ATCs to a corresponding flight. """
def flight_online_atc_form(request):
    arrivaldeparture = request.POST[KEY.FLIGHT_ONLINE_ATC_FORM_ARRIVALDEPARTURE]
    flight_id = request.POST[KEY.FLIGHT_ONLINE_ATC_FORM_FLIGHT_ID]
    online_atc_ids = request.POST.getlist(KEY.FLIGHT_ONLINE_ATC_CHECK_BOXES)

    model = None
    if str(arrivaldeparture) == str(AOD.ARRIVAL):
        model = ArrivalFlight
    if str(arrivaldeparture) == str(AOD.DEPARTURE):
        model = DepartureFlight

    flight = model.objects.get(pk=flight_id)
    flight.online_atcs.clear()
    
    if len(online_atc_ids) > 0:
        for online_atc_id in online_atc_ids:
            atc = AirTrafficController.objects.get(pk=online_atc_id)
            flight.online_atcs.add(atc)

    return HttpResponseRedirect(reverse("airport_management:index"))

""" Function to add lane to corresponding flight. """
def flight_lane_form(request):
    arrivaldeparture = request.POST[KEY.FLIGHT_LANE_FORM_ARRIVALDEPARTURE]
    flight_id = request.POST[KEY.FLIGHT_LANE_FORM_FLIGHT_ID]
    lane_id = None
    lane = None

    try:
        lane_id = request.POST[KEY.FLIGHT_LANE_RADIOS]
        lane = Lane.objects.get(pk=lane_id)
    except MultiValueDictKeyError as error:
        print(error)

    model = None
    if str(arrivaldeparture) == str(AOD.ARRIVAL):
        model = ArrivalFlight
    if str(arrivaldeparture) == str(AOD.DEPARTURE):
        model = DepartureFlight

    flight = model.objects.get(pk=flight_id)
    flight.lane = lane
    flight.save()

    return HttpResponseRedirect(reverse("airport_management:index"))

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
        airport_manager_group = create_or_get_group(
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