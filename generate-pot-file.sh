#!/bin/sh
# This script generates the po/nautilus-admin.pot file
FILEPATH="$(readlink -f "$0")"
DIR="$(dirname "$FILEPATH")"
cd "$DIR"
xgettext --package-name=nautilus-admin --package-version=0.1.2 -cTRANSLATORS \
         "extension/nautilus-admin.py" -o "po/nautilus-admin.pot"
