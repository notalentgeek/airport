# Script to re-make the database models.

#!/bin/sh

# Get this script current directory.
BASEDIR=$(dirname $0) &&
echo "set the base directory into ${BASEDIR}"

# Identify the models of applications.
python3 -B "${BASEDIR}/../manage.py" makemigrations airport_management &&
echo "made migrations for the airport management application" &&
# Create the models for whole project.
python3 -B "${BASEDIR}/../manage.py" migrate &&
echo "re-created the models for the whole django project"