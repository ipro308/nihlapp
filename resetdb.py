import os

os.system("rm db/dev.db")
os.system("python manage.py syncdb --noinput")
os.system("python manage.py loaddata fixtures/auth.json fixtures/core.json")
