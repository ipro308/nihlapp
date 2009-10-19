#!/bin/sh

rm db/dev.db
python manage.py syncdb --noinput
python manage.py loaddata fixtures/auth.json fixtures/core.json

