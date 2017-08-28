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
echo "loaded lanes fixtures"