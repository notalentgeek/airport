# Script to re-make the database models.

#!/bin/sh

# Get this script current directory.
BASEDIR=$(dirname $0) &&
echo "set the base directory into ${BASEDIR}"

# Identify the models of applications.
python3 "${BASEDIR}/manage.py" makemigrations airport_management &&
echo "make migrations for the airport management application" &&
# Create the models for whole project.
python3 "${BASEDIR}/manage.py" migrate &&
echo "re-create the models for the whole django project"