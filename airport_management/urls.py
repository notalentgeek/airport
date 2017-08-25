from django.conf.urls import url

from . import views

app_name = "airport_management"
urlpatterns = [
    url(r"^$", views.index, name="index"),
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
        name="register_airport_manager")
]