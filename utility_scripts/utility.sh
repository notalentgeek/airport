# Combination scripts to delete all migrations, then re-make the database
# models.

#!/bin/sh

# Get this script current directory.
BASEDIR=$(dirname $0) &&
echo "set the base directory into ${BASEDIR}" &&

# Make other scripts to be executable.
chmod +x "${BASEDIR}/remove_and_reset.sh" &&
chmod +x "${BASEDIR}/migrations.sh" &&
chmod +x "${BASEDIR}/load_fixtures.sh" &&

# Reset.
"${BASEDIR}/remove_and_reset.sh" &&

# Migrate.
"${BASEDIR}/migrations.sh" &&

# Load fixtures.
"${BASEDIR}/load_fixtures.sh"