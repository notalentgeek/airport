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
* This is personal my run file to make sure `docker-compose` ran good. However, this completely stop running container and deletes all images in the machine. Execute this from project's root.

```markdown
sudo ./automation/r.sh
./automation/rm.sh
sudo rm celerybeat.pid
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi -f $(docker images -a -q)
docker-compose stop
yes | docker-compose rm
yes | docker-compose rm nginx
yes | docker-compose rm web
docker-compose build
docker-compose up -d
docker-compose up
```

* ./automation/rm.sh is used to reset all database and clean directories (deleting .pyc, ...) before putting fixtures back to database.