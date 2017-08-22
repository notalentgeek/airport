from django.conf.urls import url

from . import views

app_name = "airport_management"
urlpatterns = [
    url(r"^$", views.index, name="index")
]