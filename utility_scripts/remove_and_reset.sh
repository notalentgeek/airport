# Script to delete Python's cache and reset migrations.

#!/bin/sh

# Get this script current directory.
BASEDIR=$(dirname $0) &&
echo "set the base directory into ${BASEDIR}"

# Delete Celerybeat PID.
rm -R "${BASEDIR}/../celerybeat.pid"
echo "deleted celerybeat.pid ${BASEDIR}/../celerybeat.pid" &&

# Delete SQLite3 database.
rm "${BASEDIR}/../db.sqlite3"
echo "deleted the sqlite3 database at ${BASEDIR}/../db.sqlite3" &&

# Delete all Python compiled files. This is the better way.
find ${BASEDIR}/.. | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
echo "delete all compiled python files"

# Delete virtual environment directory.
rm -R "${BASEDIR}/../venv"
echo "deleted virtual environment folder ${BASEDIR}/../venv" &&

# Replace `"lane": false` and `"lane": true` into `"lane": null`.
find "${BASEDIR}/../airport_management/fixtures/airport_management" -type f \
    -print0 | xargs -0 sed -i \
    's/"lane": false/"lane": null/g'
find "${BASEDIR}/../airport_management/fixtures/airport_management" -type f \
    -print0 | xargs -0 sed -i \
    's/"lane": true/"lane": null/g'
echo "reset fixtures" &&

# Reset NGINX log.
>${BASEDIR}/../logs/nginx-access.log &&
>${BASEDIR}/../logs/nginx-error.log &&
echo "reset nginx logs"