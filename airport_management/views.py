from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

AIRPORT_MANAGER_GROUP = "airport_manager"

# Create your views here.
def check_user_existence(request):
    username = request.GET.get("username", "")
    return HttpResponse(User.objects.filter(username=username).exists())

def index(request):
    return render(request,
        "airport_management/index.html", { "user": request.user })

def login_airport_manager(request):
    user = authenticate(
        username=request.POST["username"],
        password=request.POST["password"]
    )
    if user is not None:
        if user.is_active:
            login(request, user)

    return HttpResponseRedirect(reverse("airport_management:index"))

def login_or_register_airport_manager(request):
    if request.POST["submit_button"] == "login":
        return login_airport_manager(request)
    elif request.POST["submit_button"] == "register":
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
