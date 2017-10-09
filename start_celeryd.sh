#!/bin/bash

# Shell script to start `celeryd`. It is used to executes Celery tasks. Here
# I set the `--loglevel=DEBUG` and `--verbosity=2` so that better output can
# be seen in the terminal.

# Wait a bit for RabbitMQ to ready.
sleep 20

cd /home/airport/mount_point/
python manage.py celeryd