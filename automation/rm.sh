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