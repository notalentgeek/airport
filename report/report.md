# API and Database Models

![./schema.png](schema.png)

[./schema.dia](schema.dia)

This is an airport application for incoming and outcoming flights from/to Schipol airport. The flights data is taken everyday at midnight from Schipol official airport API. The API data provided from the Schipol API has rich variation of keys, but their values in incomplete. Sometimes there are keys that just blank or null. Furthermore, there are little to no information on what each keys describes. Despite the two sole main issues, I chose to use this API because it is free and provides the most number of API pulls out of other options that are available.

The main models is the `ArrivalDepartureFlight` model, which then inherited further to `ArrivalFlight` and `DepartureFlight` models. Initially they have unique fields like destined/origin airport and scheduled time for arrival and departure. However, I realize that the API only provides data from the Schipol airport side. Which means one other airport is always Schipol. The API does not provide time for flight's operation with the other airport. So in then end, both `ArrivalFlight` and `DepartureFlight` come from `ArrivalDepartureFlight` without any unique field, just each stored in different tables.

Flight code, carrier's code, an airport, and scheduled time can be taken directly from the API. I only need to make a function to determine the day for each flights. There is many-to-many field for flight to be attached by air traffic controller (ATC). There is also many-to-many field for lane, for the flight later operates. The status field is a null-boolean field, with `null` when the flight is being in operation, `true` if the flight operation completed with an ATC and lane attached to the flight, and return `false` if, at most, one of the two elements is missing. During the development, I planned to have `real_local_time` and `past_atcs` as well. But I scrapped these to further simplify the development progress.

Both `ArrivalFlight` and `DepartureFlight` is filled initially from the Schipol API pull. However, ATC and lane are inputted manually by the user (airport manager).

The `Lane` models is just as a list of available runways in Schipol airport. This information is taken from Sciphol Wikipedia page, [here](https://en.wikipedia.org/wiki/Amsterdam_Airport_Schiphol).

The other model is the `AirTrafficController`, often referred as "ATC" in some comments inside the codes. It only has three characters fields: code, first name, and last name. The `AirTrafficController` is supplied by logged-in airport manager via "ATC Registration Form" in the client user interface.

The last model I created is called `CeleryWorker`. It is used to queue task in Celery task queue. This is necessary to prevent database locked because this project currently using SQLite as database, where multiple connection should not happen.

# Details of the Requirements

An ATC and lane need to be attached to a arrival or departure flight before their scheduled operation time happen. Otherwise the flight status will be `false`. Additionally, the client user interface will tell the airport manager if a flight lacks of ATC or lane (or both).

At first there was a form to input the flight data manually. Now, Schipol API automatically take care of that. The Schipol API, I think, is rather young and under-developed. When I asked the admin, on why the API only return 20 objects at max per day they answered theoretically. However, they could not provide technical details (how-to with programming language) on how to pull more than 20 objects at time. In the end, I made a custom Python script to automatically pull maximum data the API provide (nearly ~400 flights per day for both arrival and departure flights, cargo and non-cargo flights) and sent back my script to them.

The ATC is not assigned automatically by the system. The airport managers need to manually do that. However, at simplest it can be done with system detecting which ATCs has least workload (lesser amount of managed flight on average) and assign that ATC to an incoming operation. Even further, it system could detect if tha airport need more ATCs and if a certain flight needs more than one ATCs. Initially, I wanted to remove ATCs from finished operation, but that will take more time to develop.

The data provided from the API and data from the airport manager are shown in a simple table with pagination. Sort function does not exists. This is because I could not understand how the table library works for AJAX request. Hence, I made my own flight tables with Bootstrap. However, there is no summarization on overall operation in whole. So to sum up, the information is displayed only within this SPA with tables (for ATCs and flights) and a management panel that displays more information about selected flight.

At this point, if data is not exist (deleted via admin control panel) it will return 404 error. There are only three notifications exists if the airport manager do an error within the client user interface: when user inputted wrong username and password combination, when user tried to register airport manager username that is already in database, and when user tried to register an ATC which has its code already in database.

# Application Structure and Schema

![./structure.png](structure.png)

[./structure.dia](structure.dia)

The diagram shows all process and static files used to run this application.

The main "protagonist" here is Django, the all-in-one, "batteries included" solution for full-stack web developer. Django basically provides all routings and simple interface to database (SQLite). Django also connected to Celery, which will be discussed in later paragraph, that is meant to manage task with respect to real-life timing (year, month, ...).

Django has a `collectstatic` command to put every necessary static files to one folder for easier access for NGINX.

Celery is a Python task scheduler, to execute Python function based on real-life time. To work, Celery needs a message broker and by default it sets to use RabbitMQ.

Message broker is a process to translate message from one protocol to another. RabbitMQ here is used to get timing from the host OS task scheduler: like `cron` in UNIX or whatever it is in Windows. With connection to `cron` RabbitMQ can let Celery to have timings on when to execute tasks.

For this application there are three tasks: to pull API, to check existing flight data, and to save database to fixtures (static JSON file). They are scheduled at daily, per-minute, and every ten minutes, respectively.

Both NGINX and Gunicorn are a HTTP server that serve different purposes. NGINX is used to serve static files and to route interactive HTTP requests to Gunicorn. Gunicorn is used to handle dynamic HTTP request to a running Django process. Hence, some says, the whole process is faster, because one server is used to handle static files, whereas requests, which take longer to execute, will be handled with different server (Gunicorn).

NGINX is the last process in the operating system before requests and responds go to the Internet.

# Key Directories and Files

* ./Dockerfile as an init file for Docker container.
* ./airport_management/fixtures/airport_management/css for JSON version of the database.
* ./airport_management/http_requests_views.py for handling view that are related to HTTP request from client.
* ./airport_management/models.py for all database models.
* ./airport_management/static/airport_management/css for CSS.
* ./airport_management/static/airport_management/js for controllers.
* ./airport_management/tasks.py for all Celery tasks.
* ./airport_management/transit_view.py for view that redirects back to index page.
* ./airport_management/views.py for index view (since this is an SPA, there is only one view).
* ./docker-compose.yml as an init file for services necessary to launch this web application.