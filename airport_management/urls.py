from django.conf.urls import url

from . import views

app_name = "airport_management"
urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(
        r"^check_air_traffic_controller_code_existence/$",
        views.check_air_traffic_controller_code_existence,
        name="check_air_traffic_controller_code_existence"
    ),
    url(r"^check_user_existence/$", views.check_user_existence,
        name="check_user_existence"),
    url(r"^login_airport_manager/$", views.login_airport_manager,
        name="login_airport_manager"),
    url(
        r"^login_or_register_airport_manager/$",
        views.login_or_register_airport_manager,
        name="login_or_register_airport_manager"
    ),
    url(r"^logout_airport_manager/$", views.logout_airport_manager,
        name="logout_airport_manager"),
    url(r"^register_airport_manager/$", views.register_airport_manager,
        name="register_airport_manager"),
    url(r"^register_atc/$", views.register_atc,
        name="register_atc"),
    url(r"^request_table_pagination/$", views.request_table_pagination,
        name="request_table_pagination")
]