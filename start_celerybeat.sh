#!/bin/bash

# Shell script to start `celerybeat`. It is used to manage timing on Celery
# tasks.

# Wait a bit for RabbitMQ to ready.
sleep 20

cd /home/airport/mount_point/
python manage.py celerybeat