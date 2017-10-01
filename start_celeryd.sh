#!/bin/bash

sleep 20
cd /app
python manage.py celeryd --loglevel=DEBUG --verbosity=2