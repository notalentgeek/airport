# Combination scripts to delete all migrations, then re-make the database
# models.

#!/bin/sh

# Get this script current directory.
BASEDIR=$(dirname $0) &&
echo "set the base directory into ${BASEDIR}" &&

# Make other scripts to be executable.
chmod +x "${BASEDIR}/reset.sh" &&
chmod +x "${BASEDIR}/makemigrations_and_migrate.sh" &&

# Reset.
"${BASEDIR}/reset.sh"
"${BASEDIR}/mm.sh"
# Migrate.

$SHELL