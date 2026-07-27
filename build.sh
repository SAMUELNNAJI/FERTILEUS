#!/usr/bin/env bash
# =============================================================
#  FertilEus – Production Build Script
#  Run once on each deploy: installs deps, migrates, collects static.
#  Usage: bash build.sh
# =============================================================

set -o errexit   # Exit immediately if any command fails
set -o nounset   # Treat unset variables as errors
set -o pipefail  # Catch errors in piped commands

echo "-----> Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "-----> Running database migrations..."
python manage.py migrate --no-input

echo "-----> Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "-----> Build complete."
