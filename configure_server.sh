#!/usr/bin/env bash

mv core_content.sql IEDCSServer

cd IEDCSServer

echo "Make migrations..."
python manage.py makemigrations

echo ""
echo "Migrate..."
python manage.py migrate

echo ""
echo "Create new Administrator..."
python manage.py createsuperuser

echo ""
echo "Load sql data..."
sqlite3 db.sqlite3 ".read core_content.sql"

echo "Server configured!"
