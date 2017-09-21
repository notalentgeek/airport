"""
Function to check existence of a value in an attribute in a model table.
"""

from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.db.models import Max, Min
from django.http import HttpResponse

def check_existence(
    request,
    key_name,       # Key name from the client.
    model,          # Model to look up.
    key_name_filter # Key name from the model.
):
    value = request.GET.get(key_name, "")
    return HttpResponse(model.objects.filter(**{ key_name_filter:value })\
        .exists())

""" A function to create or get group (Django). """
def create_or_get_group(group_name):
    try:
        return Group.objects.create(name=group_name)
    except IntegrityError as error:
        return Group.objects.get(name=group_name)

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