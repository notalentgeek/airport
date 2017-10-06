# Accessing

* Application: [http://.../airport_management](http://.../airport_management).
* Admin Control Panel: [http://.../admin](http://.../admin) for this example you can use username: admin and password: asdasdasd.

# How to run this application:

* This is personal my run commands to make sure `docker-compose` ran good. HOWEVER, this completely stop running container and deletes all images in the machine. Execute this from project's root. I would suggest to look for instruction further below.

```markdown
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi -f $(docker images -a -q)
sudo ./utility_scripts/remove_and_reset.sh
./utility_scripts/utility.sh
docker-compose stop
yes | docker-compose rm
yes | docker-compose rm nginx
yes | docker-compose rm web
docker-compose build
docker-compose up -d
docker-compose up
```

* Similar run commands but for in DigitalOcean directly from root (I know it is not good XD).

```markdown
cd /root
git clone https://github.com/notalentgeek/airport.git --depth 1
cp /root/airport/airport.service /etc/systemd/system
systemctl enable airport.service
apt-get install python3-pip
export LC_ALL=C
pip3 install -r /root/airport/requirements.txt
reboot
```

* `export LC_ALL=C` is used to set locale to proceed with `pip3` installation. This will not be necessary if a user is registered.

## __Generally__, ./utility_scripts/utility.sh needs to be ran before `docker-compose build`.
* You can either use local `runserver`, local Gunicorn/NGINX, or with contained in Docker.
* Make sure NGINX and RabbitMQ installed.
* Copy paste ./host_nginx/nginx.conf to /etc/nginx/nginx.conf (perhaps, create backup first and then copy with super user privilege).
* Make sure to register specific user for RabbitMQ.
* For running in local.
    * Start NGINX, `sudo service nginx start`.
    * Start RabbitMQ, `sudo service rabbitmq-server start`.
* For running in container.
    * Stop NGINX, `sudo service nginx stop`.
    * Stop RabbitMQ, `sudo service rabbitmq-server stop`.
* Go to settings.py.
    * Here you need to adjust the RabbitMQ's username, password, and `vhost` (for virtual host, but `vhost` is optional).
    * If this is ran with Django's `runserver`.
        * Comment the multi-lines `BROKER_URL`.
        * Un-comment the one line `BROKER_URL`.
        * `DEBUG=True` if this is ran with Django's `runserver`.
    * If this is in a Docker container or if this is ran with Gunicorn/NGINX.
        * Comment the one line `BROKER_URL`.
        * Un-comment the multi-lines `BROKER_URL`.
        * `DEBUG=False` if in a Docker container or if this is ran with Gunicorn/NGINX.
* Go to tasks.py.
    * Here, it is all depends whether you want to have Celery executing all tasks or just to pull flights API.
    * For pulling flights API.
        * Comment `check_this_minute_flights_status()`'s decorator.
        * Comment `create_backup_fixtures_()`'s decorator.
        * Comment `flight_api_pull()`'s decorator.
        * Un-comment `flight_api_pull_()`'s decorator.
    * For production and full fledged-testing.
        * Un-comment `check_this_minute_flights_status()`'s decorator.
        * Un-comment `create_backup_fixtures_()`'s decorator.
        * Un-comment `flight_api_pull()`'s decorator.
        * Comment `flight_api_pull_()`'s decorator.
* Go to start_web.sh.
    * If this is ran on host/local machine.
        * Comment `python manage.py collectstatic --noinput`.
        * Un-comment `python3 manage.py collectstatic --noinput`.
    * If this is ran in container.
        * Comment `python3 manage.py collectstatic --noinput`.
        * Un-comment `python manage.py collectstatic --noinput`.
* To run.
    * With virtual environment.
        * Make sure `virtualenv` is installed.
        * Go to root of this application project directory and run `python3 -m virtualenv venv`.
        * Run ` source ./venv/bin/activate`.
        * Run `pip3 install -r ./requirements.txt`.
        * Go to `start_web.sh` and switch (comment/un-comment) the `# Start Gunicorn!` part.
        * With `runserver`.
            * Run `python3 manage.py celerybeat`.
            * Run `python3 manage.py celeryd`.
            * Run `python3 manage.py runserver`.
        * With Gunicorn/NGINX.
            * Run `chmod +x start_celery.sh`.
            * Run `chmod +x start_web.sh`.
            * Run `./start_celery.sh`.
            * Run `./start_web.sh`.
    * With `docker-compose`.
        * (Optional) there are some trouble shootings if `docker-compose` returns an error (PLEASE PROCEED WITH CAUTION).
            * Run `docker rm $(docker ps -a -q)` to remove all container.
            * Run `docker rmi -f $(docker images -a -q)`. to remove all un-tagged images.
            * Run `docker stop $(docker ps -a -q)` to stop all running container.
            * Run `docker-compose stop` to stop running compose in current active directory.
            * Run `yes | docker-compose rm nginx` delete running container with "nginx" listed as its name.
            * Run `yes | docker-compose rm web` delete running container with "web" listed as its name.
            * Run `yes | docker-compose rm` delete running container.
        * Run `sudo rm celerybeat.pid`.
        * Run `docker-compose build`.
        * Run `docker-compose up -d`.
        * Run `docker-compose up`.

# Basic troubleshooting:

* If there are missing static files (CSS, JS, images, ...) in production or when `DEBUG=False` try to run `python3 manage.py collectstatic --noinput` to migrate back the assets.
* Make sure to migrate first before initiating the container. There is no way to launch Celery after migration finished. Hence it is better to run the migration before initiating the container. `./utility_scripts/utility.sh` can be used to clear the project from unnecessary files.
* Port used for this application: 5672 for RabbitMQ, 8080 for NGINX, for 15672 for RabbitMQ interface.
* Sometimes celerybeat.pid exists in project root. This file is a result of celerybeat process being force killed. This file needs to be deleted in order for the celerybeat to run.

# Utilities:

* ./utility_scripts/utility.sh can be used to clean directories (deleting .pyc, ...), reset all database, reset NGINX logs, before then putting fixtures back to database.

# Known bugs:

* Celery does not update task schedule despite `...schedule updated` in `celeryd`. This bug is referred by this ticket [https://github.com/celery/django-celery-beat/issues/7](https://github.com/celery/django-celery-beat/issues/7).
* `celerybeat` stuck with error message, `...task not taking effect...`, [https://github.com/celery/django-celery-beat/issues/7](https://github.com/celery/django-celery-beat/issues/7). Some say, upgrading to Celery 4.x solve the problem. However, Django Celery only works Celery 3.1.25.

# To-do List:

* A lot of closures needs to be made in the tasks.py.
* Change ATC and lane entry to AJAX like request instead to prevent full page reload.
* For some reason there are files created from the container owned by root, this should not happen.
* In ideal case scenario, docker-compose.yml should be able to be put with some arguments. However AFAIK, you can only put arguments in the Dockerfile.
* Make the add ATCs and add lane requests done through AJAX. Adding the data one-by-one and then web-page refresh is extremely annoying.
* Unit testing.