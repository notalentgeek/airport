# Script to delete Python's cache and reset migrations.

#!/bin/sh

# Get this script current directory.
BASEDIR=$(dirname $0) &&
echo "set the base directory into ${BASEDIR}"

# Delete the SQLite3 database.
rm "${BASEDIR}/../db.sqlite3"
echo "deleted the sqlite3 database at ${BASEDIR}/../db.sqlite3" &&

# Delete the main project Python's cache.
rm -R "${BASEDIR}/../airport/__pycache__"
echo "deleted the python's cache at ${BASEDIR}/../airport/__pycache__" &&

# Delete the airport_management migrations and Python's cache.
rm -R "${BASEDIR}/../airport_management/migrations"
echo "deleted the django migrations directory at\
    ${BASEDIR}/../airport_management/migrations" &&
rm -R "${BASEDIR}/../airport_management/__pycache__"
echo "deleted the python's cache at\
    ${BASEDIR}/../airport_management/__pycache__" &&
rm -R "${BASEDIR}/../airport_management/src/__pycache__"
echo "deleted the python's cache at\
    ${BASEDIR}/../airport_management/src/__pycache__"