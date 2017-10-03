#!/bin/bash

# PENDING: From the source here,
# http://tutos.readthedocs.io/en/latest/source/ndg.html it says that it is a
# common practice to have a specific user to handle the webserver.

SCRIPT=$(readlink -f "$0")
DJANGO_SETTINGS_MODULE=airport.settings
DJANGO_WSGI_MODULE=airport.wsgi
NAME="airport"
NUM_WORKERS=3

if [ "$SCRIPT" = "/" ]
then
    BASEDIR=""
else
    BASEDIR=$(dirname "$SCRIPT")
fi

if [ "$BASEDIR" = "/" ]
then
    SQLITE="db.sqlite3"
else
    SQLITE=${BASEDIR}"/db.sqlite3"
fi

if [ "$BASEDIR" = "/" ]
then
    VENV_BIN="venv/bin"
    SOCKFILE="run/gunicorn.sock"
else
    VENV_BIN=${BASEDIR}"/venv/bin"
    SOCKFILE=${BASEDIR}"/run/gunicorn.sock"
fi

SOCKFILEDIR="$(dirname "$SOCKFILE")"
VENV_ACTIVATE=${VENV_BIN}"/activate"
VENV_GUNICORN=${VENV_BIN}"/gunicorn"

# Activate the virtual environment.
# Only set this for virtual environment.
#cd $BASEDIR
#source $VENV_ACTIVATE

# Set environment variables.
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$PYTHONPATH:$BASEDIR

# Create run directory if they does not exists.
test -d $SOCKFILEDIR || mkdir -p $SOCKFILEDIR

# Start fresh!
./automation/rm.sh

# Start Gunicorn!
# Programs meant to be run under supervisor should not daemonize themselves
# (do not use --daemon).
#
# Set this for virtual environment.
#exec ${VENV_GUNICORN} ${DJANGO_WSGI_MODULE}:application \
#    --bind=unix:$SOCKFILE \
#    --name $NAME \
#    --workers $NUM_WORKERS

# For non-virtual environment.
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
    --bind=unix:$SOCKFILE \
    --name $NAME \
    --workers $NUM_WORKERS