# Combination scripts to delete all migrations, then re-make the database
# models.

#!/bin/sh

# Get this script current directory.
BASEDIR=$(dirname $0) &&
echo "set the base directory into ${BASEDIR}" &&

# Make other scripts to be executable.
chmod +x "${BASEDIR}/r.sh" &&
chmod +x "${BASEDIR}/mm.sh" &&
chmod +x "${BASEDIR}/f.sh" &&

# Reset.
"${BASEDIR}/r.sh" &&
# Migrate.
"${BASEDIR}/mm.sh" &&
# Load fixtures.
"${BASEDIR}/f.sh"

# PENDING: Put this into separate files.

# Replace `"lane": false` and `"lane": true` into `"lane": null`.
find "${BASEDIR}/../airport_management/fixtures/airport_management" -type f \
    -print0 | xargs -0 sed -i \
    's/"lane": false/"lane": null/g'
find "${BASEDIR}/../airport_management/fixtures/airport_management" -type f \
    -print0 | xargs -0 sed -i \
    's/"lane": true/"lane": null/g'