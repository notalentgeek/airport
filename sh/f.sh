# Script to load fixtures.

#!/bin/sh

# Get this script current directory.
BASEDIR=$(dirname $0) &&
echo "set the base directory into ${BASEDIR}" &&

# Load administration fixture.
python3 -B ${BASEDIR}/../manage.py loaddata airport_management/admin.json &&
echo "loaded administration fixtures" &&
# Load lanes fixture.
python3 -B ${BASEDIR}/../manage.py loaddata airport_management/lanes.json &&
echo "loaded lanes fixtures" &&
# Load arrival fixture this fixture may not exists.
python3 -B ${BASEDIR}/../manage.py\
    loaddata airport_management/arrival_flight.json
echo "loaded arrival fixtures" &&
# Load departure fixture this fixture may not exists.
python3 -B ${BASEDIR}/../manage.py\
    loaddata airport_management/departure_flight.json
echo "loaded departure fixtures"