from django.conf.urls import url

from . import http_requests_views
from . import transit_views
from . import views

app_name = "airport_management"
urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(
        r"^check_airport_manager_name_existence/$",
        transit_views.check_airport_manager_name_existence,
        name="check_airport_manager_name_existence"
    ),
    url(
        r"^check_atc_code_existence/$",
        transit_views.check_atc_code_existence,
        name="check_atc_code_existence"
    ),
    url(
        r"^airport_manager_login_and_registration_form/$",
        transit_views.airport_manager_login_and_registration_form,
        name="airport_manager_login_and_registration_form"
    ),
    url(r"^login_airport_manager/$", transit_views.login_airport_manager,
        name="login_airport_manager"),
    url(r"^register_airport_manager/$", transit_views.register_airport_manager,
        name="register_airport_manager"),
    url(r"^logout_airport_manager/$", transit_views.logout_airport_manager,
        name="logout_airport_manager"),
    url(r"^register_atc/$", transit_views.register_atc,
        name="register_atc"),
    url(
        r"^flight_atc_form/$",
        http_requests_views.flight_atc_form,
        name="flight_atc_form"
    ),
    url(
        r"^pagination_request_flight_table/$",
        http_requests_views.pagination_request_flight_table,
        name="pagination_request_flight_table"
    ),
    url(
        r"^table_requests_flight/$",
        http_requests_views.table_requests_flight,
        name="table_requests_flight"
    )
]